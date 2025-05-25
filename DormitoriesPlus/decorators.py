from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "נדרשת התחברות כדי לגשת לדף זה.")
                return redirect('login_page')
            
            if request.user.role not in allowed_roles:
                messages.error(request, "אין לך הרשאה לגשת לדף זה.")
                return redirect('login_page')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 