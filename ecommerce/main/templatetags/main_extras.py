from django import template

register = template.Library()

@register.simple_tag
def discount(a , b):
    return a - b
@register.simple_tag
def discount_percentage(a, b):
    return int(b / a * 100) 

