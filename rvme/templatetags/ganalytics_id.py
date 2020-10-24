from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def ganalytics_id():
    return settings.GOOGLE_ANALYTICS_ID