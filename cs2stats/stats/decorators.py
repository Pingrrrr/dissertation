from django.http import HttpResponse
from django.shortcuts import redirect

#https://www.youtube.com/watch?v=eBsc65jTKvw&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=15&t=515s

def unauthenicated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('dashboard')
        return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            print('Working:', allowed_roles)
            return view_func (request, *args, **kwargs)
        return wrapper_func
    return decorator