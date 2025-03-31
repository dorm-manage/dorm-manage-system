from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import (
    User,
    InventoryTracking,
    Item,
    Request,
    Building,
    Message,
    RoomAssignment
)
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    if request.method == 'POST':
        # איסוף נתונים מהטופס
        full_name = request.POST.get('name')  # נניח שמדובר בשם מלא
        id_number = request.POST.get('id_number')
        building_number = request.POST.get('building_number')
        apartment_number = request.POST.get('apartment_number')
        product = request.POST.get('product')
        time_needed = request.POST.get('time_needed')
        room_num = f"{building_number}-{apartment_number}"

        # שימוש במשתמש המחובר – במידה והמשתמש לא מחובר, יש לטפל במצב בהתאם
        user = request.user if request.user.is_authenticated else None

        # ניסיון למצוא מוצר במלאי לפי שם הפריט (בהנחה שהשם תואם ל-inventory)
        try:
            inventory_item = InventoryTracking.objects.get(item_name=product)
            # חיפוש פריט זמין במלאי
            available_item = Item.objects.filter(inventory_id=inventory_item.item_id, status='available').first()
        except InventoryTracking.DoesNotExist:
            available_item = None

        # יצירת רשומת בקשה מסוג השאלת ציוד
        new_request = Request.objects.create(
            user=user,
            request_type='equipment_rental',
            item_id=available_item.item_id if available_item else None,
            room_num=room_num,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        # במידה ויש פריט זמין – עדכון סטטוס
        if available_item:
            available_item.status = 'borrowed'
            available_item.updated_at = timezone.now()
            available_item.save()

        messages.success(request, "בקשת השאלת הציוד נרשמה בהצלחה!")
        return redirect('application')
    return render(request, 'application.html')


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
