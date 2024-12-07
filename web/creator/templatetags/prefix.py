from django import template

register = template.Library()


@register.filter('prefix')
def prefix(text, prefix):
    return prefix + str(text)
