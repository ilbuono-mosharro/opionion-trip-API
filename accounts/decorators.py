import functools

from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def authentication_not_required(view_func, redirect_url="pages:home"):
    """
        this decorator ensures that a user is not logged in,
        if a user is logged in, the user will get redirected to
        the url whose view name was passed to the redirect_url parameter
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'You need to be logged out')
        return redirect(redirect_url)

    return wrapper


def ajax_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
