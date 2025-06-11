from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import datetime
from django.utils.safestring import mark_safe
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.shortcuts import render, redirect
from django.db.models import Count, Q, Prefetch
from django.db import transaction
from django.contrib.auth.models import User
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
    return render(request, 'OM_Homepage.html')


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

    # Define min and max return dates
    min_return_date = (timezone.now() + timezone.timedelta(days=1)).date().strftime('%Y-%m-%d')
    # Set max return date as end_date or 1 year from now if no end_date
    if end_date:
        max_return_date = min(end_date, (timezone.now() + timezone.timedelta(days=365)).date())
    else:
        max_return_date = (timezone.now() + timezone.timedelta(days=365)).date()
    max_return_date = max_return_date.strftime('%Y-%m-%d')

    if request.method == 'POST':
        item_id = request.POST.get('product')
        return_date = request.POST.get('return_date')
        loan_days = (datetime.strptime(return_date, '%Y-%m-%d').date() - timezone.now().date()).days
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

                # Check if the loan period extends beyond the student's room assignment
                if end_date and datetime.strptime(return_date, '%Y-%m-%d').date() > end_date:
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

            # Find the highest ID in the table
            max_id = InventoryTracking.objects.all().order_by(
                '-id').first().id if InventoryTracking.objects.exists() else 0

            # Create inventory tracking record with a guaranteed unique ID
            inventory_item = InventoryTracking.objects.create(
                id=max_id + 1,  # Force a unique ID
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

    # Initialize items_by_inventory as a dictionary with default sub-dictionaries
    items_by_inventory = {}


    # Get all items and group them by inventory
    items_list = Item.objects.all().select_related('inventory')

    # Group items by inventory item and status
    for item in items_list:
        if item.inventory_id not in items_by_inventory:
            # Initialize with default values to avoid KeyError
            items_by_inventory[item.inventory_id] = {
                'available': 0,
                'borrowed': 0,
                'total': 0
            }

        # Increment the appropriate status counter
        if item.status in ['available', 'borrowed']:
            items_by_inventory[item.inventory_id][item.status] += 1

        # Increment total counter
        items_by_inventory[item.inventory_id]['total'] += 1

    # Pagination
    paginator = Paginator(inventory_list, 25)  # Show 25 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'BM_inventory.html', {
        'inventory': page_obj,
        'items_by_inventory': items_by_inventory,
        'page_obj': page_obj,
    })

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
                    # Remove the item completely
                    if req_obj.item:
                        # Store the item info for the success message
                        item_name = req_obj.item.inventory.item_name if req_obj.item.inventory else "הפריט"
                        # Delete the item
                        req_obj.item.delete()
                        # Set item to None to avoid reference errors
                        req_obj.item = None
                        messages.success(request, f"{item_name} הוסר מהמלאי בהצלחה.")

                        req_obj.updated_at = timezone.now()
                        req_obj.save()

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



@login_required
def BM_manage_students(request):
    # Get the building manager (current user)
    bm = request.user

    # Get buildings managed by this building manager (one query)
    managed_buildings = Building.objects.filter(building_staff_member=bm)

    if not managed_buildings.exists():
        # Early return if no buildings are managed
        return render(request, 'BM_manage_students.html', {
            'buildings_data': [],
            'managed_buildings': [],
        })

    # Get active building from query params or use the first one
    active_building_id = request.GET.get('building_id')
    if active_building_id:
        try:
            active_building_id = int(active_building_id)
        except (ValueError, TypeError):
            active_building_id = None

    if not active_building_id and managed_buildings.exists():
        active_building_id = managed_buildings.first().id

    # Handle POST requests (adding/removing students)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_student':
            # Handle adding student
            handle_add_student(request, managed_buildings)

            # Redirect to keep the active building tab
            return redirect(f"{request.path}?building_id={active_building_id}")

        elif action == 'remove_student':
            # Handle removing student
            handle_remove_student(request, managed_buildings)

            # Redirect to keep the active building tab
            return redirect(f"{request.path}?building_id={active_building_id}")

    # Prepare data for buildings (optimized for the active building)
    buildings_data = []

    # Current date for filtering assignments
    current_date = timezone.now().date()

    for building in managed_buildings:
        is_active = building.id == active_building_id

        # Basic building data (minimal for inactive buildings)
        building_data = {
            'building': building,
            'is_active': is_active,
            'available_rooms': [],
            'students_page': None,
            'has_data': False,
        }

        # Only load detailed data for the active building
        if is_active:
            # Get rooms with their capacity and occupied count in one efficient query
            rooms = Room.objects.filter(building=building).annotate(
                occupied_count=Count(
                    'assignments',
                    filter=Q(assignments__end_date__isnull=True) | Q(assignments__end_date__gte=current_date)
                ),
                room_number_int=Cast('room_number', IntegerField())
            ).order_by('room_number_int')

            # Filter and format available rooms
            available_rooms = []
            for room in rooms:
                available_spots = max(0, room.capacity - room.occupied_count)
                if available_spots > 0:
                    available_rooms.append({
                        'room': room,
                        'available_spots': available_spots
                    })

            # Get students in this building with pagination
            students_qs = RoomAssignment.objects.filter(
                room__building=building
            ).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=current_date)
            ).select_related('user', 'room').order_by('room__room_number')

            # Setup pagination
            page_size = 20  # 20 students per page
            paginator = Paginator(students_qs, page_size)
            page_number = request.GET.get(f'students_page_{building.id}', 1)
            students_page = paginator.get_page(page_number)

            # Update building data
            building_data.update({
                'available_rooms': available_rooms,
                'students_page': students_page,
                'students_count': students_qs.count(),  # Just the count for UI
                'has_data': True,
            })

        buildings_data.append(building_data)

    context = {
        'buildings_data': buildings_data,
        'managed_buildings': managed_buildings,
        'active_building_id': active_building_id,
    }

    return render(request, 'BM_manage_students.html', context)


def handle_add_student(request, managed_buildings):
    """
    Handle adding a new student - separated to keep main view cleaner
    """
    # Get form data
    room_id = request.POST.get('room_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    id_number = request.POST.get('id_number', '')  # Optional ID number
    password = request.POST.get('password', '123456789')  # Default password if none provided
    end_date_str = request.POST.get('end_date')

    # If password is empty, use the default
    if not password or not password.strip():
        password = '123456789'

    # Validate input
    if not all([room_id, first_name, last_name, email, end_date_str]):
        messages.error(request, "אנא מלא את כל השדות הנדרשים.")
        return False

    try:
        # Parse end date
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Check if room belongs to one of the manager's buildings
        room = Room.objects.get(
            id=room_id,
            building__in=managed_buildings
        )

        # Check if room has capacity
        current_assignments_count = RoomAssignment.objects.filter(
            room=room
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=timezone.now().date())
        ).count()

        if current_assignments_count >= room.capacity:
            messages.error(request, "אין מקום פנוי בחדר זה.")
            return False

        # Use a transaction to ensure all related DB operations succeed or fail together
        with transaction.atomic():
            # Check if user already exists
            try:
                user = User.objects.get(email=email)

                # Update existing user's details
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password)  # Set new password
                user.save()

            except User.DoesNotExist:
                # Create new user
                user = User.objects.create_user(
                    email=email,
                    username=email,  # Using email as username
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role='student'
                )

            # Create room assignment
            assignment = RoomAssignment.objects.create(
                user=user,
                room=room,
                start_date=timezone.now().date(),
                end_date=end_date,
                assigned_at=timezone.now()
            )

        messages.success(request,
                         f"הסטודנט {first_name} {last_name} שובץ בהצלחה לחדר {room.room_number} בבניין {room.building.building_name} עד לתאריך {end_date_str}.")
        return True

    except Room.DoesNotExist:
        messages.error(request, "החדר שנבחר אינו קיים או שאין לך הרשאה לנהל אותו.")
    except ValueError:
        messages.error(request, "פורמט תאריך לא תקין. אנא השתמש בפורמט YYYY-MM-DD.")

    return False


def handle_remove_student(request, managed_buildings):
    """
    Handle removing a student - separated to keep main view cleaner
    """
    assignment_id = request.POST.get('assignment_id')
    delete_user = request.POST.get('delete_user') == 'yes'

    try:
        # Verify the assignment belongs to a room in one of the manager's buildings
        assignment = RoomAssignment.objects.select_related('user', 'room__building').get(
            id=assignment_id,
            room__building__in=managed_buildings
        )

        user = assignment.user

        # Check if the student has any borrowed items
        borrowed_items = Request.objects.filter(
            user=user,
            request_type='equipment_rental',
            status='approved'
        ).select_related('item__inventory')

        # If there are borrowed items and it's not a force removal
        if borrowed_items.exists() and not request.POST.get('force_remove'):
            borrowed_items_count = borrowed_items.count()
            # Create a detailed message about borrowed items
            items_details = [f"{req.item.inventory.item_name} (מושאל מתאריך {req.updated_at.strftime('%d/%m/%Y')})"
                             for req in borrowed_items]
            items_list = ", ".join(items_details)

            error_message = f"""
            <div class="borrowed-warning">
                <p><strong>לסטודנט יש {borrowed_items_count} פריטים מושאלים שטרם הוחזרו:</strong></p>
                <p>{items_list}</p>
                <p>האם ברצונך להסיר את הסטודנט ולסמן את כל הפריטים כמוחזרים?</p>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <a href="{request.path}?building_id={assignment.room.building.id}" class="button" style="background-color: #6c757d; text-decoration: none; padding: 8px 12px; border-radius: 5px; color: white;">ביטול</a>
                    <form method="POST" action="{request.path}" style="display: inline;">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" value="remove_student">
                        <input type="hidden" name="assignment_id" value="{assignment.id}">
                        <input type="hidden" name="force_remove" value="yes">
                        <input type="hidden" name="delete_user" value="{request.POST.get('delete_user', 'no')}">
                        <input type="hidden" name="building_id" value="{assignment.room.building.id}">
                        <button type="submit" class="remove-button">הסר ומחזר פריטים</button>
                    </form>
                </div>
            </div>
            """
            # Mark the message as safe HTML
            messages.error(request, mark_safe(error_message))
            return False

        # Use a transaction to ensure all related DB operations succeed or fail together
        with transaction.atomic():
            # If force remove with borrowed items, mark all items as returned
            if borrowed_items.exists() and request.POST.get('force_remove'):
                # Update all borrowed items in a single query
                borrowed_item_ids = borrowed_items.values_list('id', flat=True)

                # Update request status
                Request.objects.filter(id__in=borrowed_item_ids).update(
                    status='resolved',
                    updated_at=timezone.now()
                )

                # Update item status to available
                item_ids = Request.objects.filter(id__in=borrowed_item_ids).values_list('item_id', flat=True)
                Item.objects.filter(id__in=item_ids).update(
                    status='available',
                    updated_at=timezone.now()
                )

            # Delete the assignment (or end it)
            if delete_user:
                # Get user info for success message before deletion
                user_full_name = f"{user.first_name} {user.last_name}"

                # Delete all assignments for this user
                RoomAssignment.objects.filter(user=user).delete()

                # Delete the user
                user.delete()

                messages.success(request, f"הסטודנט {user_full_name} הוסר מהמערכת ונמחק בהצלחה.")
            else:
                # Just end the assignment
                assignment.end_date = timezone.now().date()
                assignment.save(update_fields=['end_date'])

                messages.success(request,
                                 f"הסטודנט {user.first_name} {user.last_name} הוסר מחדר {assignment.room.room_number}.")

        return True

    except RoomAssignment.DoesNotExist:
        messages.error(request, "שיבוץ החדר לא נמצא או שאין לך הרשאה להסיר אותו.")

    return False


# Add these views to your views.py file

@login_required
def OM_Homepage(request):
    # Get the office manager (current user)
    om = request.user

    # Get all buildings
    all_buildings = Building.objects.all()

    # Count total students
    total_students = User.objects.filter(role='student', is_active=True).count()

    # Calculate occupancy rate - based on room assignments
    total_rooms = Room.objects.count()
    # Count rooms that have at least one assignment
    occupied_rooms = Room.objects.annotate(
        assignment_count=Count('assignments')
    ).filter(assignment_count__gt=0).count()
    occupancy_rate = int((occupied_rooms / total_rooms * 100)) if total_rooms > 0 else 0

    # Count late items (equipment rentals past due date)
    current_date = timezone.now()
    # Assuming items are late after 7 days if no due_date field exists
    late_items = Request.objects.filter(
        request_type='equipment_rental',
        status='approved',
        created_at__lt=current_date - timezone.timedelta(days=7)
    ).count()

    # Count only open faults (not including those in progress)
    open_faults = Request.objects.filter(
        request_type='fault_report',
        status='open'  # Only count 'open' status, not 'pending' or 'in_progress'
    ).count()

    # Get recent urgent faults (high urgency) from all buildings
    urgent_faults = Request.objects.filter(
        request_type='fault_report',
        urgency='גבוהה',
        status__in=['open', 'pending']
    ).select_related('user', 'room').order_by('-created_at')[:5]

    # Additional data for other parts of the template
    pending_requests_count = Request.objects.filter(
        request_type='equipment_rental',
        status='pending'
    ).count()

    borrowed_items_count = Request.objects.filter(
        request_type='equipment_rental',
        status='approved'
    ).count()

    pending_faults_count = Request.objects.filter(
        request_type='fault_report',
        status='pending'
    ).count()

    context = {
        # New real statistics for the cards
        'total_students': total_students,
        'occupancy_rate': occupancy_rate,
        'late_items': late_items,
        'open_faults': open_faults,

        # Additional data for other parts of the template
        'pending_requests_count': pending_requests_count,
        'borrowed_items_count': borrowed_items_count,
        'pending_faults_count': pending_faults_count,
        'urgent_faults': urgent_faults,
        'all_buildings': all_buildings,
    }

    return render(request, 'OM_homepage.html', context)


@login_required
def OM_inventory(request):
    # This is similar to BM_inventory but without building filtering
    # Handle form submissions for inventory management
    if request.method == 'POST':
        # Add new inventory item
        if 'add_item' in request.POST:
            item_name = request.POST.get('item_name')
            quantity = int(request.POST.get('quantity'))
            photo = request.FILES.get('photo', None)

            # Find the highest ID in the table
            max_id = InventoryTracking.objects.all().order_by(
                '-id').first().id if InventoryTracking.objects.exists() else 0

            # Create inventory tracking record with a guaranteed unique ID
            inventory_item = InventoryTracking.objects.create(
                id=max_id + 1,  # Force a unique ID
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

        return redirect('OM_inventory')

    # Get all inventory items
    inventory_list = InventoryTracking.objects.all().order_by('-updated_at')

    # Initialize items_by_inventory as a dictionary with default sub-dictionaries
    items_by_inventory = {}

    # Get all items and group them by inventory
    items_list = Item.objects.all().select_related('inventory')

    # Group items by inventory item and status
    for item in items_list:
        if item.inventory_id not in items_by_inventory:
            # Initialize with default values to avoid KeyError
            items_by_inventory[item.inventory_id] = {
                'available': 0,
                'borrowed': 0,
                'total': 0
            }

        # Increment the appropriate status counter
        if item.status in ['available', 'borrowed']:
            items_by_inventory[item.inventory_id][item.status] += 1

        # Increment total counter
        items_by_inventory[item.inventory_id]['total'] += 1

    # Pagination
    paginator = Paginator(inventory_list, 25)  # Show 25 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'OM_inventory.html', {
        'inventory': page_obj,
        'items_by_inventory': items_by_inventory,
        'page_obj': page_obj,
    })


@login_required
def OM_loan_requests(request):
    # Similar to BM_loan_requests but with access to all buildings

    # Get all pending equipment rental requests
    pending_requests_list = Request.objects.filter(
        request_type='equipment_rental',
        status='pending'
    ).select_related('user', 'item', 'room').order_by('-created_at')

    # Get borrowed (approved but not returned) equipment requests
    borrowed_items_list = Request.objects.filter(
        request_type='equipment_rental',
        status='approved'
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

            # Process request (Office Manager can handle all buildings)
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
                # Remove the item completely
                if req_obj.item:
                    # Store the item info for the success message
                    item_name = req_obj.item.inventory.item_name if req_obj.item.inventory else "הפריט"
                    # Delete the item
                    req_obj.item.delete()
                    # Set item to None to avoid reference errors
                    req_obj.item = None
                    messages.success(request, f"{item_name} הוסר מהמלאי בהצלחה.")

            # Save the comment as admin note
            if admin_comment:
                req_obj.admin_note = admin_comment

            req_obj.updated_at = timezone.now()
            req_obj.save()

            messages.success(request, "הבקשה עודכנה בהצלחה!")

            # Preserve the active tab after form submission
            if action in ['return', 'damaged']:
                return redirect(f"{reverse('OM_loan_requests')}#borrowed-items")
            else:
                return redirect('OM_loan_requests')
        except Request.DoesNotExist:
            messages.error(request, "בקשה לא נמצאה!")
            return redirect('OM_loan_requests')

    context = {
        'pending_requests': pending_page_obj,
        'borrowed_items': borrowed_page_obj,
        'available_counts': available_counts,
    }

    return render(request, 'OM_loan_requests.html', context)


@login_required
def OM_faults(request):
    # Similar to BM_faults but with access to all buildings

    # Get open fault reports from all buildings
    open_fault_reports = Request.objects.filter(
        request_type='fault_report',
        status='open'
    ).select_related('user', 'room', 'room__building').order_by('-created_at')

    # Get pending fault reports from all buildings
    pending_fault_reports = Request.objects.filter(
        request_type='fault_report',
        status='pending'
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

            # Update status based on action (OM can handle all buildings)
            if action in ['pending', 'resolved']:
                fault.status = action

            # Add admin comment if provided
            if admin_comment:
                # If there's already an admin note, append the new comment
                if fault.admin_note:
                    fault.admin_note = f"{fault.admin_note}\n{timezone.now().strftime('%d/%m/%Y %H:%M')} - {admin_comment}"
                else:
                    fault.admin_note = f"{timezone.now().strftime('%d/%m/%Y %H:%M')} - {admin_comment}"

            fault.updated_at = timezone.now()
            fault.save()

            messages.success(request, "התקלה עודכנה בהצלחה!")

        except Request.DoesNotExist:
            messages.error(request, "תקלה לא נמצאה!")

        # Redirect back to the page, maintaining the correct tab
        return redirect('OM_faults')

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

    return render(request, 'OM_faults.html', context)


@login_required
def OM_manage_students(request):
    # Similar to BM_manage_students but with all-buildings access

    # Get all buildings
    all_buildings = Building.objects.all()

    if not all_buildings.exists():
        # Early return if no buildings exist
        return render(request, 'OM_manage_students.html', {
            'buildings_data': [],
            'all_buildings': [],
        })

    # Get active building from query params or use the first one
    active_building_id = request.GET.get('building_id')
    if active_building_id:
        try:
            active_building_id = int(active_building_id)
        except (ValueError, TypeError):
            active_building_id = None

    if not active_building_id and all_buildings.exists():
        active_building_id = all_buildings.first().id

    # Handle POST requests (adding/removing students)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_student':
            # Handle adding student - office manager can add to any building
            handle_add_student_OM(request, all_buildings)

            # Redirect to keep the active building tab
            return redirect(f"{request.path}?building_id={active_building_id}")

        elif action == 'remove_student':
            # Handle removing student - office manager can remove from any building
            handle_remove_student_OM(request, all_buildings)

            # Redirect to keep the active building tab
            return redirect(f"{request.path}?building_id={active_building_id}")

    # Prepare data for buildings (optimized for the active building)
    buildings_data = []

    # Initialize stats counters
    total_students_count = 0
    total_capacity = 0
    total_occupied = 0
    total_empty_slots = 0
    ending_this_month = 0

    # Current date for filtering assignments
    current_date = timezone.now().date()
    # End of current month for filtering assignments ending this month
    month_end = current_date.replace(day=28)
    if month_end.month == 12:
        next_month = datetime.date(month_end.year + 1, 1, 1)
    else:
        next_month = datetime.date(month_end.year, month_end.month + 1, 1)
    month_end = next_month - datetime.timedelta(days=1)

    for building in all_buildings:
        is_active = building.id == active_building_id

        # Basic building data (minimal for inactive buildings)
        building_data = {
            'building': building,
            'is_active': is_active,
            'available_rooms': [],
            'students_page': None,
            'has_data': False,
        }

        # Get rooms with their capacity and occupied count for stats
        rooms = Room.objects.filter(building=building).annotate(
            occupied_count=Count(
                'assignments',
                filter=Q(assignments__end_date__isnull=True) | Q(assignments__end_date__gte=current_date)
            ),
            room_number_int=Cast('room_number', IntegerField())
        )

        # Calculate stats for this building
        building_capacity = sum(room.capacity for room in rooms)
        building_occupied = sum(room.occupied_count for room in rooms)
        building_empty_slots = sum(max(0, room.capacity - room.occupied_count) for room in rooms)

        # Add to the totals
        total_capacity += building_capacity
        total_occupied += building_occupied
        total_empty_slots += building_empty_slots

        # Only load detailed data for the active building
        if is_active:
            # Filter and format available rooms
            available_rooms = []
            for room in rooms.order_by('room_number_int'):
                available_spots = max(0, room.capacity - room.occupied_count)
                if available_spots > 0:
                    available_rooms.append({
                        'room': room,
                        'available_spots': available_spots
                    })

            # Get students in this building with pagination
            students_qs = RoomAssignment.objects.filter(
                room__building=building
            ).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=current_date)
            ).select_related('user', 'room').order_by('room__room_number')

            # Count students ending this month
            ending_this_month_count = RoomAssignment.objects.filter(
                room__building=building,
                end_date__gte=current_date,
                end_date__lte=month_end
            ).count()

            ending_this_month += ending_this_month_count

            # Setup pagination
            page_size = 20  # 20 students per page
            paginator = Paginator(students_qs, page_size)
            page_number = request.GET.get(f'students_page_{building.id}', 1)
            students_page = paginator.get_page(page_number)

            # Update building data
            building_data.update({
                'available_rooms': available_rooms,
                'students_page': students_page,
                'students_count': students_qs.count(),  # Just the count for UI
                'has_data': True,
            })

        buildings_data.append(building_data)

    # Calculate total students count and average occupancy
    total_students_count = total_occupied
    avg_occupancy = int((total_occupied / total_capacity * 100)) if total_capacity > 0 else 0

    context = {
        'buildings_data': buildings_data,
        'all_buildings': all_buildings,
        'active_building_id': active_building_id,
        # Stats for dashboard
        'total_students_count': total_students_count,
        'avg_occupancy': avg_occupancy,
        'total_empty_slots': total_empty_slots,  # New stat - total empty slots instead of available rooms
        'ending_this_month': ending_this_month,
    }

    return render(request, 'OM_manage_students.html', context)


# Helper functions for OM_manage_students - similar to BM functions but for all buildings
def handle_add_student_OM(request, all_buildings):
    """
    Handle adding a new student for Office Manager - can add to any building
    """
    # Get form data
    room_id = request.POST.get('room_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    id_number = request.POST.get('id_number', '')  # Optional ID number
    password = request.POST.get('password', '123456789')  # Default password if none provided
    end_date_str = request.POST.get('end_date')

    # If password is empty, use the default
    if not password or not password.strip():
        password = '123456789'

    # Validate input
    if not all([room_id, first_name, last_name, email, end_date_str]):
        messages.error(request, "אנא מלא את כל השדות הנדרשים.")
        return False

    try:
        # Parse end date
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Check if room exists - Office Manager can access any room
        room = Room.objects.get(id=room_id)

        # Check if room has capacity
        current_assignments_count = RoomAssignment.objects.filter(
            room=room
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=timezone.now().date())
        ).count()

        if current_assignments_count >= room.capacity:
            messages.error(request, "אין מקום פנוי בחדר זה.")
            return False

        # Use a transaction to ensure all related DB operations succeed or fail together
        with transaction.atomic():
            # Check if user already exists
            try:
                user = User.objects.get(email=email)

                # Update existing user's details
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password)  # Set new password
                user.save()

            except User.DoesNotExist:
                # Create new user
                user = User.objects.create_user(
                    email=email,
                    username=email,  # Using email as username
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role='student'
                )

            # Create room assignment
            assignment = RoomAssignment.objects.create(
                user=user,
                room=room,
                start_date=timezone.now().date(),
                end_date=end_date,
                assigned_at=timezone.now()
            )

        messages.success(request,
                         f"הסטודנט {first_name} {last_name} שובץ בהצלחה לחדר {room.room_number} בבניין {room.building.building_name} עד לתאריך {end_date_str}.")
        return True

    except Room.DoesNotExist:
        messages.error(request, "החדר שנבחר אינו קיים.")
    except ValueError:
        messages.error(request, "פורמט תאריך לא תקין. אנא השתמש בפורמט YYYY-MM-DD.")

    return False


def handle_remove_student_OM(request, all_buildings):
    """
    Handle removing a student for Office Manager - can remove from any building
    """
    assignment_id = request.POST.get('assignment_id')
    delete_user = request.POST.get('delete_user') == 'yes'

    try:
        # Get the assignment - Office Manager can remove from any building
        assignment = RoomAssignment.objects.select_related('user', 'room__building').get(id=assignment_id)

        user = assignment.user

        # Check if the student has any borrowed items
        borrowed_items = Request.objects.filter(
            user=user,
            request_type='equipment_rental',
            status='approved'
        ).select_related('item__inventory')

        # If there are borrowed items and it's not a force removal
        if borrowed_items.exists() and not request.POST.get('force_remove'):
            borrowed_items_count = borrowed_items.count()
            # Create a detailed message about borrowed items
            items_details = [f"{req.item.inventory.item_name} (מושאל מתאריך {req.updated_at.strftime('%d/%m/%Y')})"
                             for req in borrowed_items]
            items_list = ", ".join(items_details)

            error_message = f"""
            <div class="borrowed-warning">
                <p><strong>לסטודנט יש {borrowed_items_count} פריטים מושאלים שטרם הוחזרו:</strong></p>
                <p>{items_list}</p>
                <p>האם ברצונך להסיר את הסטודנט ולסמן את כל הפריטים כמוחזרים?</p>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <a href="{request.path}?building_id={assignment.room.building.id}" class="button" style="background-color: #6c757d; text-decoration: none; padding: 8px 12px; border-radius: 5px; color: white;">ביטול</a>
                    <form method="POST" action="{request.path}" style="display: inline;">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" value="remove_student">
                        <input type="hidden" name="assignment_id" value="{assignment.id}">
                        <input type="hidden" name="force_remove" value="yes">
                        <input type="hidden" name="delete_user" value="{request.POST.get('delete_user', 'no')}">
                        <input type="hidden" name="building_id" value="{assignment.room.building.id}">
                        <button type="submit" class="remove-button">הסר ומחזר פריטים</button>
                    </form>
                </div>
            </div>
            """
            # Mark the message as safe HTML
            messages.error(request, mark_safe(error_message))
            return False

        # Use a transaction to ensure all related DB operations succeed or fail together
        with transaction.atomic():
            # If force remove with borrowed items, mark all items as returned
            if borrowed_items.exists() and request.POST.get('force_remove'):
                # Update all borrowed items in a single query
                borrowed_item_ids = borrowed_items.values_list('id', flat=True)

                # Update request status
                Request.objects.filter(id__in=borrowed_item_ids).update(
                    status='resolved',
                    updated_at=timezone.now()
                )

                # Update item status to available
                item_ids = Request.objects.filter(id__in=borrowed_item_ids).values_list('item_id', flat=True)
                Item.objects.filter(id__in=item_ids).update(
                    status='available',
                    updated_at=timezone.now()
                )

            # Delete the assignment (or end it)
            if delete_user:
                # Get user info for success message before deletion
                user_full_name = f"{user.first_name} {user.last_name}"

                # Delete all assignments for this user
                RoomAssignment.objects.filter(user=user).delete()

                # Delete the user
                user.delete()

                messages.success(request, f"הסטודנט {user_full_name} הוסר מהמערכת ונמחק בהצלחה.")
            else:
                # Just end the assignment
                assignment.end_date = timezone.now().date()
                assignment.save(update_fields=['end_date'])

                messages.success(request,
                                 f"הסטודנט {user.first_name} {user.last_name} הוסר מחדר {assignment.room.room_number}.")

        return True

    except RoomAssignment.DoesNotExist:
        messages.error(request, "שיבוץ החדר לא נמצא.")

    return False


def is_operations_manager(user):
    """Check if user is an operations manager"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'OM'

@login_required
def OM_manage_BM(request):
    """
    View for office managers to manage building managers and their building assignments.
    Allows adding, updating, and viewing building manager assignments.
    """
    # Check if user is office staff
    if request.user.role != 'office_staff':
        messages.error(request, "אין לך הרשאות לגשת לעמוד זה")
        return redirect('login_page')

    # Get all buildings
    buildings = Building.objects.all().select_related('building_staff_member')

    # Get all users with building_staff role for dropdown
    building_staff_users = User.objects.filter(role='building_staff')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'assign_manager':
            building_id = request.POST.get('building_id')
            staff_user_id = request.POST.get('staff_user_id')

            try:
                # Get the building
                building = Building.objects.get(id=building_id)

                # Get the staff user
                staff_user = User.objects.get(id=staff_user_id, role='building_staff')

                # Update the building's staff member
                building.building_staff_member = staff_user
                building.updated_at = timezone.now()
                building.save()

                messages.success(request,
                                 f"אחראי {staff_user.first_name} {staff_user.last_name} שויך לבניין {building.building_name} בהצלחה")

            except Building.DoesNotExist:
                messages.error(request, "הבניין שנבחר אינו קיים")
            except User.DoesNotExist:
                messages.error(request, "המשתמש שנבחר אינו קיים או אינו אחראי בניין")

        elif action == 'remove_manager':
            building_id = request.POST.get('building_id')

            try:
                # Get the building
                building = Building.objects.get(id=building_id)

                # Check if there's a manager to remove
                if building.building_staff_member:
                    manager_name = f"{building.building_staff_member.first_name} {building.building_staff_member.last_name}"

                    # Remove the manager
                    building.building_staff_member = None
                    building.updated_at = timezone.now()
                    building.save()

                    messages.success(request, f"אחראי {manager_name} הוסר מבניין {building.building_name} בהצלחה")
                else:
                    messages.warning(request, f"לא היה אחראי משויך לבניין {building.building_name}")

            except Building.DoesNotExist:
                messages.error(request, "הבניין שנבחר אינו קיים")

        elif action == 'add_manager':
            # Handle adding a new building manager user
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password', '123456789')  # Default password

            # Validate inputs
            if not all([first_name, last_name, email]):
                messages.error(request, "אנא מלא את כל השדות הנדרשים")
                return redirect('OM_manage_BM')

            # Check if user with email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, f"משתמש עם אימייל {email} כבר קיים במערכת")
                return redirect('OM_manage_BM')

            # Create the new user
            try:
                with transaction.atomic():
                    # Create user with building_staff role
                    new_user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        role='building_staff'
                    )

                    messages.success(request, f"אחראי בניין חדש {first_name} {last_name} נוצר בהצלחה")

                    # If a building was selected, assign the manager to it
                    building_id = request.POST.get('assign_building_id')
                    if building_id:
                        building = Building.objects.get(id=building_id)
                        building.building_staff_member = new_user
                        building.updated_at = timezone.now()
                        building.save()

                        messages.success(request,
                                         f"אחראי בניין {first_name} {last_name} שויך לבניין {building.building_name}")

            except Exception as e:
                messages.error(request, f"אירעה שגיאה ביצירת המשתמש: {str(e)}")

    context = {
        'buildings': buildings,
        'building_staff_users': building_staff_users,
    }

    return render(request, 'OM_manage_BM.html', context)

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
                return redirect('OM_Homepage')
            elif user.role == 'student':
                return redirect('Students_homepage')
            else:
                return redirect('login_page')
        else:
            messages.error(request, "שם משתמש או סיסמה לא נכונים!")
    return render(request, 'login_page.html')


def custom_logout(request):
    logout(request)
    messages.success(request, "התנתקת בהצלחה!")
    return redirect('login_page')
