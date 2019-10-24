from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re


@csrf_exempt
def simple_route(request, data=None):
    if data:
        return HttpResponse(status=404)
    elif request.method == 'GET':
        return HttpResponse('')
    elif request.method == 'PUT' or request.method == 'POST':
        return HttpResponse(status=405)


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


@csrf_exempt
def sum_get_method(request):
    if request.method == 'GET':
        a, b = request.GET.get('a'), request.GET.get('b')
        try:
            sum_ = int(a) + int(b)
        except (ValueError, TypeError):
            return HttpResponse(status=400)

        return HttpResponse(sum_)

    return HttpResponse(status=405)


@csrf_exempt
def sum_post_method(request):
    if request.method == 'POST':
        a, b = request.POST.values()
        try:
            sum_ = int(a) + int(b)
        except (ValueError, TypeError):
            return HttpResponse(status=400)

        return HttpResponse(sum_)

    return HttpResponse(status=405)
