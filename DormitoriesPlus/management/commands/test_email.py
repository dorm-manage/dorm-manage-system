from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            required=True,
            help='Email address to send test email to',
        )

    def handle(self, *args, **options):
        to_email = options['to']

        try:
            send_mail(
                'DormitoriesPlus Email Test',
                'This is a test email from your DormitoriesPlus notification system. If you receive this, your email configuration is working correctly!',
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Test email sent successfully to {to_email}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
            self.stderr.write('Please check your email configuration in settings.py and .env file')