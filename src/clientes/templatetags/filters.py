from django import template

register = template.Library()

@register.filter
def my_filter(data):
    return f'{data} - alterado pelo filter'

@register.filter
def arredonda(value, casas):
    return round(value, casas)
