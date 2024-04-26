from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def intcomma(value):
    orig = str(value)
    new = ""
    while orig != "":
        orig, digits = orig[:-3], orig[-3:]
        new = digits + "," + new if new else digits
    return new
