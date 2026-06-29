from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
    allowed_roles = [r.upper() for r in allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Silakan login terlebih dahulu untuk mengakses halaman ini.')
                return redirect('login')
            
            raw_role = str(getattr(request.user, 'role', '')).upper()
            if getattr(request.user, 'is_superuser', False):
                return view_func(request, *args, **kwargs)
                
            if 'HC' in raw_role:
                user_role = 'HC'
            elif 'IT' in raw_role:
                user_role = 'IT'
            else:
                user_role = 'TALENT'
                
            if allowed_roles and user_role not in allowed_roles:
                messages.error(request, 'Anda tidak memiliki hak akses ke halaman ini.')
                if user_role == 'HC':
                    return redirect('dashboard_hc')
                elif user_role == 'IT':
                    return redirect('dashboard_it')
                else:
                    return redirect('dashboard_talent')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def hc_required(view_func):
    return role_required(['HC'])(view_func)

def it_required(view_func):
    return role_required(['IT'])(view_func)

def talent_required(view_func):
    return role_required(['TALENT'])(view_func)
