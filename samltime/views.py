from django.conf import settings
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import djangosaml2.views


def is_safe_url_compat(url, allowed_hosts=[], **kwargs):
    try:
        allowed_hosts = list(allowed_hosts) + settings.ALLOWED_LOGIN_REDIRECT_HOSTS
    except TypeError:
        allowed_hosts = settings.ALLOWED_LOGIN_REDIRECT_HOSTS
    return is_safe_url(url, allowed_hosts=allowed_hosts, **kwargs)


djangosaml2.views.is_safe_url_compat = is_safe_url_compat


def snakex_login(request, **kwargs):
    return djangosaml2.views.login(request, **kwargs)


@require_POST
@csrf_exempt
def snakex_acs(request, *args, **kwargs):
    return djangosaml2.views.assertion_consumer_service(request, **kwargs)
