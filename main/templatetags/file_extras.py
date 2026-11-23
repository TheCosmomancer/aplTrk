import os
from django import template

register = template.Library()

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}

@register.filter
def is_image(value):
    if not value:
        return False
    return os.path.splitext(str(value))[1].lower() in IMAGE_EXTS