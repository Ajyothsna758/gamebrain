from django import template
register = template.Library()

@register.filter
def get_item(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None

@register.filter
def category_average_filter(game, category_key):
    return game.category_average(category_key)