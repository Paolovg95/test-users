from django import template
from urllib.parse import quote_plus

register = template.Library()

@register.filter
def urlencode_spaces(value):
    return quote_plus(value)
