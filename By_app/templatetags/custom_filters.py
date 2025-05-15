from django import template
from itertools import chain as itertools_chain

register = template.Library()

@register.filter
def ordinal(value):
    try:
        value = int(value)
        if 10 <= value % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
        return f"{value}{suffix}"
    except:
        return value

@register.filter
def chain(list1, list2):
    """Combine two iterables (like lists or querysets)."""
    return list(itertools_chain(list1, list2))
