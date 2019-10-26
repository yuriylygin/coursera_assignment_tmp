from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import re


@require_GET
@csrf_exempt
def simple_route(request, data=None):
    if data:
        return HttpResponse(status=404)
    else:
        return HttpResponse()


def slug_route(request, data=None):
    match = re.match(r'^([-_0-9a-z]{1,16})\/?$', data)
    if match:
        return HttpResponse(match.group(1))
    else:
        return HttpResponse(status=404)


def sum_route(request, data=None):
    match = re.match(r'^(-?[0-9]*)\/(-?[0-9]*)\/?$', data)
    if match:
        a, b = match.group(1, 2)
        sum_ = int(a) + int(b)
        return HttpResponse(sum_)
    else:
        return HttpResponse(status=404)


@require_GET
@csrf_exempt
def sum_get_method(request):
    try:
        a, b = int(request.GET.get('a')), int(request.GET.get('b'))
    except (ValueError, TypeError):
        return HttpResponse(status=400)

    return HttpResponse(a + b)


@require_POST
@csrf_exempt
def sum_post_method(request):
    try:
        a, b = int(request.POST.get('a')), int(request.POST.get('b'))
    except (ValueError, TypeError):
        return HttpResponse(status=400)

    return HttpResponse(a + b)
