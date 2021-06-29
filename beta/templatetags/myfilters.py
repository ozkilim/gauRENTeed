from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    if number == None:
        return None
    else:
        return range(int(number))


@register.filter(name='leftover')
def times(number):
    if number == None:
        return None
    else:
        return range(5 - int(number))

