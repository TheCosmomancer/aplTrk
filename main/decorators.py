from functools import wraps
from django.http import HttpResponseForbidden

def logedout_forbidden(f):
    @wraps(f)
    def _(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Forbidden')
        return f(request, *args, **kwargs)
    return _
def only_super(f):
    @wraps(f)
    def _(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden('Forbidden')
        return f(request, *args, **kwargs)
    return _