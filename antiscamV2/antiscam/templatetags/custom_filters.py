from django import template

register = template.Library()

@register.filter
def is_equal(value, other):
    return value == other
