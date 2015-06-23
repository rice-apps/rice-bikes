__author__ = 'jonathan'

from django import template
register = template.Library()

@register.filter(name='is_member')
def is_member(value, arg):
    print value
    print arg
    return arg in value

@register.filter(name='get_price')
def get_price(value, arg):
    return value[arg]['price']