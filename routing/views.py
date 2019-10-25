from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt


@require_GET
@csrf_exempt
def simple_route(request):
    return HttpResponse()


def slug_route(request, slug):
    return HttpResponse(slug)


def sum_route(request, a, b):
    try:
        a = int(a)
        b = int(b)
    except (ValueError, TypeError):
        return HttpResponse(status=400)

    return HttpResponse(a + b)


@require_GET
@csrf_exempt
def sum_get_method(request):
    try:
        a = int(request.GET.get('a'))
        b = int(request.GET.get('b'))
    except (ValueError, TypeError):
        return HttpResponse(status=400)

    return HttpResponse(a + b)


@require_POST
@csrf_exempt
def sum_post_method(request):
    try:
        a = int(request.POST.get('a'))
        b = int(request.POST.get('b'))
    except (ValueError, TypeError):
        return HttpResponse(status=400)

    return HttpResponse(a + b)

