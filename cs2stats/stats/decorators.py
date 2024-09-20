from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

#https://www.youtube.com/watch?v=eBsc65jTKvw&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=15&t=515s

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  
            
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(role in allowed_roles for role in user_groups):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper_func
    return decorator