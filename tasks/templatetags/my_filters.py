from django import template

register = template.Library()

@register.filter(name='my_range')
def my_range(start):
    res = [i+1 for i in range(start)]
    return res