__author__ = 'jonathan'

from django import template
register = template.Library()

@register.filter(name='is_member')
def is_member(value, arg):
    return arg in value

@register.filter(name='get_price')
def get_price(value, arg):
    return value[arg]['price']

@register.filter(name='get_member')
def get_member(value, arg):
    return value[arg.replace("_", " ")]

@register.filter(name='join_whitespace')
def join_whitespace(value):
    return value.replace(" ", "_")

@register.filter(name='place_whitespace')
def place_whitespace(value):
    return value.replace("_", " ")