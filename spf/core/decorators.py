from django.contrib import messages
from django.shortcuts import redirect


def unauthenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_groups=[]):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view(request, *args, **kwargs)
            elif request.user.groups.exists():
                for gn in [g.name for g in request.user.groups.all()]:
                    if gn in allowed_groups:
                        return view(request, *args, **kwargs)
                messages.warning(request, 'Página restrita.')
                return redirect('home')
        return wrapper
    return decorator