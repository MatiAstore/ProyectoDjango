from django import template 

register = template.Library()

@register.filter
def precio_tag(value):
    try:
        return "${:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value