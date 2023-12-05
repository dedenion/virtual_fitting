# your_app/templatetags/your_filter.py
from django import template

register = template.Library()

@register.filter(name='filename_from_image')
def filename_from_image(value):
    return value.split('/')[-1]
