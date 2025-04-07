from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary using the key.
    Usage: {{ my_dict|get_item:key_variable }}
    Returns default value of 0 if key doesn't exist or dictionary is not a dict.
    """
    if not isinstance(dictionary, dict):
        return 0
    return dictionary.get(key, 0)  # Default to 0 if key doesn't exist