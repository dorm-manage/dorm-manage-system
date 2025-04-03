from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return 0  # Return 0 instead of None for numeric comparisons
    return dictionary.get(key, 0)  # Default to 0 if key doesn't exist