from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(int(number))


@register.filter(name='leftover')
def times(number):
    return range(5 - int(number))
