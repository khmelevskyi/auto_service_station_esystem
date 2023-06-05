from django import template
from django.forms import CheckboxInput

register = template.Library()

@register.filter(name="remove_appname_word")
def remove_appname_word(value):
    return value.replace("website_app.","")

@register.filter(name="remove_extra_repair_part_id")
def remove_extra_repair_part_id(value):
    return value.split(" | ")[0]