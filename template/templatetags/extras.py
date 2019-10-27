from django import template

register = template.Library()


@register.filter(name='inc')
def increment(value, arg):
    return int(value) + int(arg)


@register.simple_tag
def division(a, b, **kwargs):
    a, b = int(a), int(b)
    if 'to_int' in kwargs and kwargs['to_int']:
        return int(a / b)
    else:
        return a / b

