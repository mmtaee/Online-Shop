from django import template
register = template.Library()

from main.models import MultipleImages

@register.simple_tag
def images(product):
    return MultipleImages.objects.filter(product=product)
