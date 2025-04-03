from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

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


def BM_Homepage(request):
    return render(request, 'BM_Homepage.html')


def Students_homepage(request):
    return render(request, 'Students_homepage.html')


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
                return_date = timezone.now() + timezone.timedelta(days=loan_days)

                # Check if the loan period extends beyond the student's room assignment
                if end_date and return_date.date() > end_date:
                    messages.error(request,
                                   "תקופת ההשאלה המבוקשת ארוכה יותר מתקופת המגורים שלך במעונות. אנא בחר תקופה קצרה יותר.")
                else:
                    # Create rental request with note
                    new_request = Request.objects.create(
                        user=user,
                        request_type='equipment_rental',
                        item=available_item,
                        room=room,
                        status='pending',
                        note=note,  # Save the note here
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
def faults(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        building_number = request.POST.get('building_number')
        apartment_number = request.POST.get('apartment_number')
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        room_num = f"{building_number}-{apartment_number}"
        user = request.user if request.user.is_authenticated else None

        # יצירת בקשה מסוג דיווח תקלות עם שדות נוספים (לדוגמה fault_description ו-status)
        new_fault = Request.objects.create(
            user=user,
            request_type='fault_report',
            room_num=room_num,
            fault_description=description,  # ודא שקיים שדה כזה במודל Request
            status='פתוח',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        messages.success(request, "דיווח התקלה נרשם בהצלחה!")
        return redirect('faults')
    return render(request, 'faults.html')


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
    paginator = Paginator(inventory_list, 5)  # Show 25 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'BM_inventory.html', {
        'inventory': page_obj,
        'items_by_inventory': items_by_inventory,
        'page_obj': page_obj,
    })

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


def BM_faults(request):
    if request.method == 'POST':
        fault_id = request.POST.get('fault_id')
        action = request.POST.get('action')  # 'resolve' או 'push'
        try:
            fault = Request.objects.get(pk=fault_id)
            if action == 'resolve':
                fault.status = 'resolved'  # או 'טופל' בהתאם להגדרותיך
            elif action == 'push':
                # עדכון תאריך היצירה כדי לדחוף את התקלה לראש התור
                fault.created_at = timezone.now()
            fault.updated_at = timezone.now()
            fault.save()
            messages.success(request, "התקלה עודכנה בהצלחה!")
        except Request.DoesNotExist:
            messages.error(request, "תקלה לא נמצאה!")
        return redirect('BM_faults')

    faults_list = Request.objects.filter(request_type='fault_report')
    return render(request, 'BM_faults.html', {'faults': faults_list})


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
