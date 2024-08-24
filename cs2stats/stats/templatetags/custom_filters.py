from django import template
#https://docs.djangoproject.com/en/5.1/howto/custom-template-tags/
register = template.Library()

@register.filter
def dict_key(dictionary, key):
    try:
        key = int(key)
    except (ValueError, TypeError):
        return 'Unknown Reason'
    
    return dictionary.get(key, 'Unknown Reason')

