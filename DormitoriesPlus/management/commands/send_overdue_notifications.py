import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q, F

from DormitoriesPlus.models import Request, User, Building

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send email notifications for overdue items'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            action='store_true',
            help='Actually send emails (without this flag, runs in dry-run mode)',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=0,
            help='Also notify items due in X days (for advance notification)',
        )

    def handle(self, *args, **options):
        send_emails = options['send']
        advance_days = options['days']

        today = timezone.now().date()

        # Identify overdue items (return_date < today)
        overdue_requests = Request.objects.filter(
            request_type='equipment_rental',
            status='approved',
            return_date__lt=today
        ).select_related(
            'user',
            'item__inventory',
            'room__building',
            'room__building__building_staff_member'
        )

        # If advance_days is set, also find items that will be due soon
        if advance_days > 0:
            due_soon_date = today + timezone.timedelta(days=advance_days)
            due_soon_requests = Request.objects.filter(
                request_type='equipment_rental',
                status='approved',
                return_date=due_soon_date
            ).select_related(
                'user',
                'item__inventory',
                'room__building',
                'room__building__building_staff_member'
            )
        else:
            due_soon_requests = Request.objects.none()

        # Combine the querysets if needed
        if advance_days > 0:
            all_requests = list(overdue_requests) + list(due_soon_requests)
        else:
            all_requests = list(overdue_requests)

        if not all_requests:
            self.stdout.write(self.style.SUCCESS('No overdue or soon-to-be-due items found.'))
            return

        # Group requests by student
        student_requests = {}
        bm_requests = {}

        for request in all_requests:
            # Skip if essential relationships are missing
            if not (request.user and request.item and request.item.inventory and
                    request.room and request.room.building):
                continue

            # Group by student
            if request.user.id not in student_requests:
                student_requests[request.user.id] = {
                    'user': request.user,
                    'overdue_items': [],
                    'due_soon_items': []
                }

            # Group by building manager
            bm = request.room.building.building_staff_member
            if bm and bm.id not in bm_requests:
                bm_requests[bm.id] = {
                    'bm': bm,
                    'building': request.room.building,
                    'overdue_items': [],
                    'due_soon_items': []
                }

            # Add request to the appropriate list
            item_info = {
                'request': request,
                'item_name': request.item.inventory.item_name,
                'room_number': request.room.room_number,
                'building_name': request.room.building.building_name,
                'return_date': request.return_date,
                'days_overdue': (today - request.return_date).days if request.return_date < today else 0
            }

            if request.return_date < today:
                student_requests[request.user.id]['overdue_items'].append(item_info)
                if bm:
                    bm_requests[bm.id]['overdue_items'].append(item_info)
            else:
                student_requests[request.user.id]['due_soon_items'].append(item_info)
                if bm:
                    bm_requests[bm.id]['due_soon_items'].append(item_info)

        # Send emails to students
        student_count = 0
        for student_id, student_data in student_requests.items():
            if student_data['overdue_items'] or student_data['due_soon_items']:
                self._send_student_notification(
                    student_data,
                    send_emails=send_emails,
                    advance_days=advance_days
                )
                student_count += 1

        # Send emails to building managers
        bm_count = 0
        for bm_id, bm_data in bm_requests.items():
            if bm_data['overdue_items'] or bm_data['due_soon_items']:
                self._send_bm_notification(
                    bm_data,
                    send_emails=send_emails,
                    advance_days=advance_days
                )
                bm_count += 1

        # Print summary
        overdue_count = sum(len(data['overdue_items']) for data in student_requests.values())
        due_soon_count = sum(len(data['due_soon_items']) for data in student_requests.values())

        mode = "Sent" if send_emails else "Would send"
        self.stdout.write(self.style.SUCCESS(
            f"{mode} notifications for {overdue_count} overdue items and {due_soon_count} "
            f"items due in {advance_days} days to {student_count} students and {bm_count} building managers."
        ))

    def _send_student_notification(self, student_data, send_emails=False, advance_days=0):
        user = student_data['user']
        overdue_items = student_data['overdue_items']
        due_soon_items = student_data['due_soon_items']

        # Count total items
        total_overdue = len(overdue_items)
        total_due_soon = len(due_soon_items)

        # Determine subject line based on what items they have
        if total_overdue > 0 and total_due_soon > 0:
            subject = f"DormitoriesPlus: {total_overdue} overdue items and {total_due_soon} items due soon"
        elif total_overdue > 0:
            subject = f"DormitoriesPlus: {total_overdue} overdue items requiring immediate return"
        else:
            subject = f"DormitoriesPlus: {total_due_soon} items due in {advance_days} days"

        # Prepare context for template
        context = {
            'user': user,
            'overdue_items': overdue_items,
            'due_soon_items': due_soon_items,
            'advance_days': advance_days,
            'total_overdue': total_overdue,
            'total_due_soon': total_due_soon
        }

        # Render email content
        text_content = render_to_string('emails/overdue_items_student.txt', context)
        html_content = render_to_string('emails/overdue_items_student.html', context)

        if send_emails:
            try:
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                self.stdout.write(f"Sent notification to student {user.email}")
            except Exception as e:
                self.stderr.write(f"Failed to send email to {user.email}: {str(e)}")
        else:
            self.stdout.write(f"Would send notification to student {user.email}")

    def _send_bm_notification(self, bm_data, send_emails=False, advance_days=0):
        bm = bm_data['bm']
        building = bm_data['building']
        overdue_items = bm_data['overdue_items']
        due_soon_items = bm_data['due_soon_items']

        # Count total items
        total_overdue = len(overdue_items)
        total_due_soon = len(due_soon_items)

        # Group items by student for easier review
        grouped_overdue = self._group_items_by_student(overdue_items)
        grouped_due_soon = self._group_items_by_student(due_soon_items)

        # Determine subject line
        subject = f"DormitoriesPlus: Inventory Report for {building.building_name} - {total_overdue} overdue, {total_due_soon} due soon"

        # Prepare context for template
        context = {
            'bm': bm,
            'building': building,
            'grouped_overdue': grouped_overdue,
            'grouped_due_soon': grouped_due_soon,
            'advance_days': advance_days,
            'total_overdue': total_overdue,
            'total_due_soon': total_due_soon
        }

        # Render email content
        text_content = render_to_string('emails/overdue_items_bm.txt', context)
        html_content = render_to_string('emails/overdue_items_bm.html', context)

        if send_emails:
            try:
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [bm.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                self.stdout.write(f"Sent notification to building manager {bm.email}")
            except Exception as e:
                self.stderr.write(f"Failed to send email to {bm.email}: {str(e)}")
        else:
            self.stdout.write(f"Would send notification to building manager {bm.email}")

    def _group_items_by_student(self, items):
        """Group items by student for better organization in BM emails"""
        grouped = {}
        for item in items:
            student = item['request'].user
            if student.id not in grouped:
                grouped[student.id] = {
                    'student': student,
                    'items': []
                }
            grouped[student.id]['items'].append(item)
        return grouped