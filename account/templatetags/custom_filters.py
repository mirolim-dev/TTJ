from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    return getattr(form, field_name)
