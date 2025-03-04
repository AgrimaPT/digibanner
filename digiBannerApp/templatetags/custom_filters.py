from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Check if value (converted to string) ends with the provided argument (case-insensitive)."""
    try:
        return str(value).lower().endswith(str(arg).lower())
    except Exception:
        return False
