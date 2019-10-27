from django.shortcuts import render
from django import template
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint


register = template.Library()


@register.filter
def lower(value):
    return value.lower()


@csrf_exempt
def echo(request):
    GET_params = [item for item in request.GET.items()]
    POST_params = [item for item in request.POST.items()]
    return render(request, 'echo.html', context={
        'http_method': request.method,
        'GET_params': GET_params,
        'POST_params': POST_params,
        'HTTP_X_PRINT_STATEMENT': request.META.get('HTTP_X_PRINT_STATEMENT')
    })


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
