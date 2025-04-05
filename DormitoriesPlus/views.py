from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse

# Then import your models
from .models import (
    User,
    InventoryTracking,
    Item,
    Request,
    Building,
    Message,
    RoomAssignment,
    Room  # Make sure this is included if you've created it
)

# דוגמאות עבור עמודים שאינם דורשים עיבוד טפסים
def Homepage(request):
    return render(request, 'Homepage.html')


def connect_us(request):
    return render(request, 'connect_us.html')


def Personal_erea(request):
    return render(request, 'Personal_erea.html')


def manager_Homepage(request):
    return render(request, 'manager_Homepage.html')


@login_required
def Students_homepage(request):
    user = request.user

    # Get pending and rejected loan requests
    pending_loan_requests = Request.objects.filter(
        user=user,
        request_type='equipment_rental',
        status__in=['pending', 'rejected']
    ).order_by('-created_at')

    # Get approved loan requests
    approved_requests = Request.objects.filter(
        user=user,
        request_type='equipment_rental',
        status='approved'
    ).order_by('-created_at')

    # Get open fault reports
    open_fault_reports = Request.objects.filter(
        user=user,
        request_type='fault_report',
        status='open'
    ).order_by('-created_at')

    # Get pending fault reports
    pending_fault_reports = Request.objects.filter(
        user=user,
        request_type='fault_report',
        status='pending'
    ).order_by('-created_at')

    # Get resolved fault reports
    resolved_fault_reports = Request.objects.filter(
        user=user,
        request_type='fault_report',
        status='resolved'
    ).order_by('-updated_at')

    # Handle delete request action
    if request.method == 'POST' and 'delete_request' in request.POST:
        request_id = request.POST.get('request_id')
        try:
            req = Request.objects.get(id=request_id, user=user, request_type='equipment_rental', status='rejected')
            req.delete()
            messages.success(request, "הבקשה נמחקה בהצלחה.")
        except Request.DoesNotExist:
            messages.error(request, "הבקשה לא נמצאה או שאין לך הרשאה למחוק אותה.")

    # Ensure is_due_soon and is_overdue properties will work
    for loan_request in approved_requests:
        if loan_request.return_date:
            # Calculate days remaining manually
            days_remaining = (loan_request.return_date - timezone.now().date()).days

            if days_remaining < 0:
                loan_request.days_remaining_text = "באיחור"
            elif days_remaining == 0:
                loan_request.days_remaining_text = "נותרו פחות מיום"
            elif days_remaining == 1:
                loan_request.days_remaining_text = "נותר יום אחד"
            else:
                loan_request.days_remaining_text = f"נותרו {days_remaining} ימים"
        else:
            loan_request.days_remaining_text = ""

    # Pagination for pending loan requests
    pending_paginator = Paginator(pending_loan_requests, 5)  # 5 items per page
    pending_page_number = request.GET.get('pending_page')
    pending_page_obj = pending_paginator.get_page(pending_page_number)

    # Pagination for approved requests
    approved_paginator = Paginator(approved_requests, 5)  # 5 items per page
    approved_page_number = request.GET.get('approved_page')
    approved_page_obj = approved_paginator.get_page(approved_page_number)

    # Pagination for open fault reports
    open_fault_paginator = Paginator(open_fault_reports, 5)  # 5 items per page
    open_fault_page_number = request.GET.get('open_fault_page')
    open_fault_page_obj = open_fault_paginator.get_page(open_fault_page_number)

    # Pagination for pending fault reports
    pending_fault_paginator = Paginator(pending_fault_reports, 5)  # 5 items per page
    pending_fault_page_number = request.GET.get('pending_fault_page')
    pending_fault_page_obj = pending_fault_paginator.get_page(pending_fault_page_number)

    # Pagination for resolved fault reports
    resolved_fault_paginator = Paginator(resolved_fault_reports, 5)  # 5 items per page
    resolved_fault_page_number = request.GET.get('resolved_fault_page')
    resolved_fault_page_obj = resolved_fault_paginator.get_page(resolved_fault_page_number)

    context = {
        'pending_loan_requests': pending_page_obj,
        'approved_requests': approved_page_obj,
        'open_fault_reports': open_fault_page_obj,
        'pending_fault_reports': pending_fault_page_obj,
        'resolved_fault_reports': resolved_fault_page_obj,
    }

    return render(request, 'Students_homepage.html', context)


@login_required
def application(request):
    # Get the currently logged-in user
    user = request.user

    # Get user's room assignment (assuming they have one)
    try:
        room_assignment = RoomAssignment.objects.filter(user=user).select_related('room').first()
        if room_assignment:
            room = room_assignment.room
            building = room.building
            # Get the end date of the student's room assignment
            end_date = room_assignment.end_date
        else:
            room = None
            building = None
            end_date = None
    except:
        room = None
        building = None
        end_date = None

    # Get all available items that can be borrowed
    available_items = (InventoryTracking.objects
                       .filter(item__status='available')
                       .annotate(available_count=Count('item'))
                       .filter(available_count__gt=0)
                       .distinct())

    # Define loan period options
    loan_periods = [
        {"value": "1", "display": "יום אחד"},
        {"value": "2", "display": "יומיים"},
        {"value": "3", "display": "3 ימים"},
        {"value": "7", "display": "שבוע"},
        {"value": "14", "display": "שבועיים"},
        {"value": "21", "display": "3 שבועות"},
        {"value": "30", "display": "חודש"},
        {"value": "60", "display": "חודשיים"},
        {"value": "90", "display": "3 חודשים"},
        {"value": "180", "display": "6 חודשים"},
        {"value": "365", "display": "שנה"}
    ]

    if request.method == 'POST':
        item_id = request.POST.get('product')
        loan_days = request.POST.get('loan_period')
        note = request.POST.get('note', '')  # Get the note from the form
        # Validate note length
        if len(note) > 200:
            messages.error(request, "ההערות ארוכות מדי. אנא קצר אותן ל-200 תווים או פחות.")
            return redirect('application')

        # Initialize available_item to None
        available_item = None

        # Find an available item of selected type
        try:
            inventory_item = InventoryTracking.objects.get(id=item_id)
            # Get the first available item of this type
            available_item = Item.objects.filter(inventory=inventory_item, status='available').first()

            if available_item and room:
                # Calculate return date
                loan_days = int(loan_days)
                return_date = timezone.now().date() + timezone.timedelta(days=loan_days)

                # Check if the loan period extends beyond the student's room assignment
                if end_date and return_date > end_date:
                    messages.error(request,
                                   "תקופת ההשאלה המבוקשת ארוכה יותר מתקופת המגורים שלך במעונות. אנא בחר תקופה קצרה יותר.")
                else:
                    # Create rental request with note and return date
                    new_request = Request.objects.create(
                        user=user,
                        request_type='equipment_rental',
                        item=available_item,
                        room=room,
                        status='pending',
                        note=note,  # Save the note here
                        return_date=return_date,  # Save the expected return date
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )

                    messages.success(request, "בקשת השאלת הציוד נרשמה בהצלחה! ממתין לאישור.")
                    return redirect('application')
            else:
                if not available_item:
                    messages.error(request, "הפריט אינו זמין כרגע, אנא נסה שוב מאוחר יותר.")
                if not room:
                    messages.error(request, "לא נמצא שיבוץ חדר עבורך במערכת. פנה למנהל המעונות.")
        except InventoryTracking.DoesNotExist:
            messages.error(request, "הפריט המבוקש לא נמצא.")

    # Pass relevant data to the template
    context = {
        'available_items': available_items,
        'loan_periods': loan_periods,
        'user_room': room.room_number if room else None,
        'user_building': building.building_name if building else None,
        'end_date': end_date.strftime('%d/%m/%Y') if end_date else "לא ידוע",
    }

    return render(request, 'application.html', context)

# עמוד עבור דיווח תקלות (faults.html)
@login_required
def faults(request):
    # Get the currently logged-in user
    user = request.user

    # Get user's room assignment (assuming they have one)
    try:
        room_assignment = RoomAssignment.objects.filter(user=user).select_related('room').first()
        if room_assignment:
            room = room_assignment.room
            building = room.building
        else:
            room = None
            building = None
    except:
        room = None
        building = None

    if request.method == 'POST':
        fault_type = request.POST.get('fault_type')
        fault_description = request.POST.get('fault_description')
        urgency = request.POST.get('urgency')

        if room:
            # Create fault report request
            new_fault = Request.objects.create(
                user=user,
                request_type='fault_report',
                room=room,
                fault_type=fault_type,
                fault_description=fault_description,
                urgency=urgency,
                status='open',  # Set initial status as 'open'
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            messages.success(request, "דיווח התקלה נשלח בהצלחה! הצוות יטפל בו בהקדם.")
            return redirect('Students_homepage')
        else:
            messages.error(request, "לא נמצא שיבוץ חדר עבורך במערכת. פנה למנהל המעונות.")

    # Pass relevant data to the template
    context = {
        'user_room': room.room_number if room else None,
        'user_building': building.building_name if building else None,
    }

    return render(request, 'faults.html', context)


# עמוד לשליחת הודעות לדיירים (BM_sendMassage.html)
def BM_sendMassage(request):
    if request.method == 'POST':
        building = request.POST.get('building')
        message_content = request.POST.get('message')
        # יצירת הודעה – יש ליצור את המודל Message אם אינו קיים
        Message.objects.create(
            building=building,
            content=message_content,
            created_at=timezone.now()
        )
        messages.success(request, "ההודעה נשלחה בהצלחה!")
        return redirect('BM_sendMassage')
    return render(request, 'BM_sendMassage.html')


# עמוד לניהול מלאי (BM_inventory.html)
@login_required
def BM_inventory(request):
    # Handle form submissions for inventory management
    if request.method == 'POST':
        # Add new inventory item
        if 'add_item' in request.POST:
            item_name = request.POST.get('item_name')
            quantity = int(request.POST.get('quantity'))
            photo = request.FILES.get('photo', None)

            # Create inventory tracking record
            inventory_item = InventoryTracking.objects.create(
                item_name=item_name,
                quantity=quantity,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                photo_url=photo if photo else None
            )

            # Create individual item records
            for _ in range(quantity):
                Item.objects.create(
                    inventory=inventory_item,
                    status='available',
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )

            messages.success(request, f"פריט חדש '{item_name}' נוסף בהצלחה!")

        # Remove inventory items
        elif 'remove_item' in request.POST:
            inventory_id = request.POST.get('inventory_id')
            try:
                inventory_item = InventoryTracking.objects.get(id=inventory_id)
                # Delete associated items
                Item.objects.filter(inventory=inventory_item).delete()
                # Delete inventory record
                inventory_item.delete()
                messages.success(request, "פריט הוסר בהצלחה!")
            except InventoryTracking.DoesNotExist:
                messages.error(request, "הפריט לא נמצא!")

        # Update inventory item
        elif 'update_item' in request.POST:
            inventory_id = request.POST.get('inventory_id')
            new_name = request.POST.get('new_name')
            new_quantity = int(request.POST.get('new_quantity'))
            photo = request.FILES.get('photo', None)

            try:
                inventory_item = InventoryTracking.objects.get(id=inventory_id)
                old_quantity = inventory_item.quantity

                # Update inventory record
                inventory_item.item_name = new_name
                inventory_item.quantity = new_quantity
                if photo:
                    inventory_item.photo_url = photo
                inventory_item.updated_at = timezone.now()
                inventory_item.save()

                # Handle quantity changes
                if new_quantity > old_quantity:
                    # Add new items
                    for _ in range(new_quantity - old_quantity):
                        Item.objects.create(
                            inventory=inventory_item,
                            status='available',
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                elif new_quantity < old_quantity:
                    # Remove excess items (prioritize removing 'available' items first)
                    excess_count = old_quantity - new_quantity
                    # First delete available items
                    available_items = Item.objects.filter(inventory=inventory_item, status='available')
                    if available_items.count() <= excess_count:
                        available_items.delete()
                        excess_count -= available_items.count()
                        # Then delete other items if needed
                        if excess_count > 0:
                            other_items = Item.objects.filter(inventory=inventory_item).order_by('id')[:excess_count]
                            other_items.delete()
                    else:
                        # Only delete some available items
                        available_items.order_by('id')[:excess_count].delete()

                messages.success(request, "פריט עודכן בהצלחה!")
            except InventoryTracking.DoesNotExist:
                messages.error(request, "הפריט לא נמצא!")

        # Update specific item status
        elif 'update_item_status' in request.POST:
            item_id = request.POST.get('item_id')
            new_status = request.POST.get('new_status')

            try:
                item = Item.objects.get(id=item_id)
                item.status = new_status
                item.updated_at = timezone.now()
                item.save()
                messages.success(request, f"סטטוס פריט עודכן ל-{new_status} בהצלחה!")
            except Item.DoesNotExist:
                messages.error(request, "פריט לא נמצא!")

        return redirect('BM_inventory')

    # Get all inventory items
    inventory_list = InventoryTracking.objects.all().order_by('-updated_at')
    items_list = Item.objects.all().select_related('inventory')

    # Group items by inventory item
    items_by_inventory = {}
    for item in items_list:
        if item.inventory_id not in items_by_inventory:
            items_by_inventory[item.inventory_id] = {'available': 0, 'borrowed': 0, 'damaged': 0}
        if item.status in items_by_inventory[item.inventory_id]:
            items_by_inventory[item.inventory_id][item.status] += 1

    # Pagination
    paginator = Paginator(inventory_list, 25)  # Show 25 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'BM_inventory.html', {
        'inventory': page_obj,
        'items_by_inventory': items_by_inventory,
        'page_obj': page_obj,
    })


@login_required
def BM_Homepage(request):
    # Get the building manager (current user)
    bm = request.user

    # Get buildings managed by this building manager
    managed_buildings = Building.objects.filter(building_staff_member=bm)

    # Count pending equipment rental requests from these buildings
    pending_requests_count = Request.objects.filter(
        request_type='equipment_rental',
        status='pending',
        room__building__in=managed_buildings
    ).count()

    # Count borrowed items (approved but not returned)
    borrowed_items_count = Request.objects.filter(
        request_type='equipment_rental',
        status='approved',
        room__building__in=managed_buildings
    ).count()

    # Count open fault reports
    open_faults_count = Request.objects.filter(
        request_type='fault_report',
        status='open',
        room__building__in=managed_buildings
    ).count()

    # Count pending fault reports
    pending_faults_count = Request.objects.filter(
        request_type='fault_report',
        status='pending',
        room__building__in=managed_buildings
    ).count()

    # Get recent urgent faults (high urgency)
    urgent_faults = Request.objects.filter(
        request_type='fault_report',
        urgency='גבוהה',
        status__in=['open', 'pending'],
        room__building__in=managed_buildings
    ).select_related('user', 'room').order_by('-created_at')[:5]

    context = {
        'pending_requests_count': pending_requests_count,
        'borrowed_items_count': borrowed_items_count,
        'open_faults_count': open_faults_count,
        'pending_faults_count': pending_faults_count,
        'urgent_faults': urgent_faults,
        'managed_buildings': managed_buildings,
    }

    return render(request, 'BM_Homepage.html', context)


# עמוד לניהול בקשות השאלה (BM_loan_requests.html)
@login_required
def BM_loan_requests(request):
    # Get the building manager (current user)
    bm = request.user

    # Get the buildings managed by this building manager
    managed_buildings = Building.objects.filter(building_staff_member=bm)

    # Get all pending equipment rental requests from these buildings
    pending_requests_list = Request.objects.filter(
        request_type='equipment_rental',
        status='pending',
        room__building__in=managed_buildings
    ).select_related('user', 'item', 'room').order_by('-created_at')

    # Get borrowed (approved but not returned) equipment requests
    borrowed_items_list = Request.objects.filter(
        request_type='equipment_rental',
        status='approved',
        room__building__in=managed_buildings
    ).select_related('user', 'item', 'room').order_by('-updated_at')

    # Pagination for pending requests - 10 items per page
    pending_paginator = Paginator(pending_requests_list, 10)
    pending_page_number = request.GET.get('pending_page')
    pending_page_obj = pending_paginator.get_page(pending_page_number)

    # Pagination for borrowed items - 10 items per page
    borrowed_paginator = Paginator(borrowed_items_list, 10)
    borrowed_page_number = request.GET.get('borrowed_page')
    borrowed_page_obj = borrowed_paginator.get_page(borrowed_page_number)

    # Get count of available items for each inventory type
    available_counts = {}
    for req in pending_page_obj:
        if req.item and req.item.inventory:
            inventory_id = req.item.inventory.id
            if inventory_id not in available_counts:
                # Count available items of this type
                available_counts[inventory_id] = Item.objects.filter(
                    inventory=req.item.inventory,
                    status='available'
                ).count()

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')  # 'approve', 'reject', 'return', or 'damaged'
        admin_comment = request.POST.get('comment', '')  # Get comment from the existing form

        try:
            req_obj = Request.objects.get(pk=request_id)

            # Only process if this is a request from the BM's building
            if req_obj.room and req_obj.room.building in managed_buildings:
                if action == 'approve':
                    # Update request status
                    req_obj.status = 'approved'
                    # Update the item status to borrowed
                    if req_obj.item:
                        req_obj.item.status = 'borrowed'
                        req_obj.item.save()
                    # Note: Return date is already set by the student when they made the request
                elif action == 'reject':
                    req_obj.status = 'rejected'
                elif action == 'return':
                    # Mark the request as resolved
                    req_obj.status = 'resolved'
                    # Update the item status to available
                    if req_obj.item:
                        req_obj.item.status = 'available'
                        req_obj.item.save()
                elif action == 'damaged':
                    # Mark the request as resolved
                    req_obj.status = 'resolved'
                    # Update the item status to damaged
                    if req_obj.item:
                        req_obj.item.status = 'damaged'
                        req_obj.item.save()

                # Save the comment as admin note
                if admin_comment:
                    req_obj.admin_note = admin_comment

                req_obj.updated_at = timezone.now()
                req_obj.save()

                messages.success(request, "הבקשה עודכנה בהצלחה!")

                # Preserve the active tab after form submission
                if action in ['return', 'damaged']:
                    return redirect(f"{reverse('BM_loan_requests')}#borrowed-items")
                else:
                    return redirect('BM_loan_requests')
            else:
                messages.error(request, "אין לך הרשאה לעדכן בקשות מבניינים אחרים!")
                return redirect('BM_loan_requests')
        except Request.DoesNotExist:
            messages.error(request, "בקשה לא נמצאה!")
            return redirect('BM_loan_requests')

    context = {
        'pending_requests': pending_page_obj,
        'borrowed_items': borrowed_page_obj,
        'available_counts': available_counts,
    }

    return render(request, 'BM_loan_requests.html', context)


@login_required
def BM_faults(request):
    # Get the building manager (current user)
    bm = request.user

    # Get buildings managed by this building manager
    managed_buildings = Building.objects.filter(building_staff_member=bm)

    # Get open fault reports
    open_fault_reports = Request.objects.filter(
        request_type='fault_report',
        status='open',
        room__building__in=managed_buildings
    ).select_related('user', 'room', 'room__building').order_by('-created_at')

    # Get pending fault reports
    pending_fault_reports = Request.objects.filter(
        request_type='fault_report',
        status='pending',
        room__building__in=managed_buildings
    ).select_related('user', 'room', 'room__building').order_by('-updated_at')

    # Calculate days elapsed for each pending fault report
    current_date = timezone.now().date()
    for fault in pending_fault_reports:
        days_elapsed = (current_date - fault.created_at.date()).days
        if days_elapsed == 0:
            fault.days_elapsed_text = "מהיום"
        elif days_elapsed == 1:
            fault.days_elapsed_text = "יום אחד"
        else:
            fault.days_elapsed_text = f"{days_elapsed} ימים"

    # Handle POST requests for updating faults
    if request.method == 'POST':
        fault_id = request.POST.get('fault_id')
        action = request.POST.get('action')  # 'pending', 'resolved', or 'comment'
        admin_comment = request.POST.get('admin_comment', '')

        try:
            fault = Request.objects.get(pk=fault_id)

            # Only process if this is a fault from the BM's building
            if fault.room and fault.room.building in managed_buildings:
                # Update status based on action
                if action in ['pending', 'resolved']:
                    fault.status = action

                # Add admin comment if provided (for both action='comment' and other actions)
                if admin_comment:
                    # If there's already an admin note, append the new comment
                    if fault.admin_note:
                        fault.admin_note = f"{fault.admin_note}\n{timezone.now().strftime('%d/%m/%Y %H:%M')} - {admin_comment}"
                    else:
                        fault.admin_note = f"{timezone.now().strftime('%d/%m/%Y %H:%M')} - {admin_comment}"

                fault.updated_at = timezone.now()
                fault.save()

                messages.success(request, "התקלה עודכנה בהצלחה!")
            else:
                messages.error(request, "אין לך הרשאה לעדכן תקלות מבניינים אחרים!")

        except Request.DoesNotExist:
            messages.error(request, "תקלה לא נמצאה!")

        # Redirect back to the page, maintaining the correct tab
        return redirect('BM_faults')

    # Pagination for open faults - 10 items per page
    open_page_number = request.GET.get('open_page')
    open_paginator = Paginator(open_fault_reports, 10)
    open_page_obj = open_paginator.get_page(open_page_number)

    # Pagination for pending faults - 10 items per page
    pending_page_number = request.GET.get('pending_page')
    pending_paginator = Paginator(pending_fault_reports, 10)
    pending_page_obj = pending_paginator.get_page(pending_page_number)

    context = {
        'open_fault_reports': open_page_obj,
        'pending_fault_reports': pending_page_obj,
    }

    return render(request, 'BM_faults.html', context)


# עמוד ניהול חדרים – דוגמה לשיבוץ סטודנט לחדר (manage_room.html)
def manage_room(request):
    if request.method == 'POST':
        room = request.POST.get('room')  # ניתן לאסוף את מספר החדר מהטופס או מהקונטקסט
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        faculty = request.POST.get('faculty')

        # חיפוש או יצירת משתמש בהתאם לאימייל
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'password_hash': 'hashed_dummy',  # יש להחליף בהצפנה אמיתית
                'role': 'student'
            }
        )
        # יצירת רשומת שיבוץ חדר – יש ליצור מודל RoomAssignment בהתאם
        RoomAssignment.objects.create(
            user=user,
            building=room.split('-')[0],  # לדוגמה, נניח שהחדר בפורמט "בניין-חדר"
            room=room,
            assigned_at=timezone.now()
        )
        messages.success(request, f"הסטודנט שובץ בהצלחה לחדר {room}!")
        return redirect('manage_room')
    return render(request, 'manage_room.html')


# עמוד ניהול מלאי (manager_inventory.html)
def manager_inventory(request):
    if request.method == 'POST':
        # הבחנה בין טופס הוספת פריט לטופס הסרת פריט לפי שם הכפתור
        if 'add_item' in request.POST:
            item_name = request.POST.get('item_name')
            quantity = int(request.POST.get('quantity'))
            InventoryTracking.objects.create(
                item_name=item_name,
                quantity=quantity,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            messages.success(request, "פריט חדש נוסף בהצלחה!")
        elif 'remove_item' in request.POST:
            remove_item = request.POST.get('remove_item')
            remove_quantity = int(request.POST.get('remove_quantity'))
            try:
                inventory_item = InventoryTracking.objects.get(item_name=remove_item)
                inventory_item.quantity = max(inventory_item.quantity - remove_quantity, 0)
                inventory_item.updated_at = timezone.now()
                inventory_item.save()
                messages.success(request, "פריט הוסר בהצלחה!")
            except InventoryTracking.DoesNotExist:
                messages.error(request, "הפריט לא נמצא!")
        return redirect('manager_inventory')

    inventory_list = InventoryTracking.objects.all()
    return render(request, 'manager_inventory.html', {'inventory': inventory_list})


# עמוד עדכון אחראי בניין (manager_BM.html)
def manager_BM(request):
    if request.method == 'POST':
        building_number = request.POST.get('building-number')
        manager_name = request.POST.get('manager-name')
        phone_number = request.POST.get('phone-number')
        start_date = request.POST.get('start-date')
        try:
            building = Building.objects.get(building_id=building_number)
            # לדוגמה: חיפוש משתמש לפי שם – יש להתאים זאת בהתאם ללוגיקה שלך
            user = User.objects.filter(first_name__icontains=manager_name).first()
            if user:
                building.building_staff_member = user.user_id
                building.updated_at = timezone.now()
                building.save()
                messages.success(request, "אחראי הבניין עודכן בהצלחה!")
            else:
                messages.error(request, "אחראי לא נמצא!")
        except Building.DoesNotExist:
            messages.error(request, "בניין לא נמצא!")
        return redirect('manager_BM')

    building_list = Building.objects.all()
    return render(request, 'manager_BM.html', {'buildings': building_list})


# עמוד ניהול תקלות (manager_faults.html)
def manager_faults(request):
    if request.method == 'POST':
        fault_id = request.POST.get('fault_id')
        action = request.POST.get('action')
        try:
            fault = Request.objects.get(pk=fault_id)
            if action == 'resolve':
                fault.status = 'טופל'
            fault.updated_at = timezone.now()
            fault.save()
            messages.success(request, "התקלה עודכנה בהצלחה!")
        except Request.DoesNotExist:
            messages.error(request, "תקלה לא נמצאה!")
        return redirect('manager_faults')

    faults_list = Request.objects.filter(request_type='fault_report')
    return render(request, 'manager_faults.html', {'faults': faults_list})


def Manager_request(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')  # 'approve' or 'reject'
        try:
            req_obj = Request.objects.get(pk=req_id)
            if action == 'approve':
                req_obj.status = 'מאושרת'
            elif action == 'reject':
                req_obj.status = 'נדחתה'
            req_obj.updated_at = timezone.now()
            req_obj.save()
            messages.success(request, "הבקשה עודכנה בהצלחה!")
        except Request.DoesNotExist:
            messages.error(request, "בקשה לא נמצאה!")
        return redirect('Manager_request')

    requests_list = Request.objects.filter(request_type='equipment_rental')
    return render(request, 'Manager_request.html', {'requests': requests_list})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # הפניה בהתאם לתפקיד המשתמש:
            if user.role == 'building_staff':
                return redirect('BM_Homepage')
            elif user.role == 'office_staff':
                return redirect('manager_Homepage')
            elif user.role == 'student':
                return redirect('Students_homepage')
            else:
                return redirect('login')
        else:
            messages.error(request, "שם משתמש או סיסמה לא נכונים!")
    return render(request, 'login_page.html')


def custom_logout(request):
    logout(request)
    messages.success(request, "התנתקת בהצלחה!")
    return redirect('login')
