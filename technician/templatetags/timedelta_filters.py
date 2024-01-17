# timedelta_filters.py
from django import template
register = template.Library()
@register.filter
def format_timedelta(value):
    if value is None:
        return ''

    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    result = ''
    if days > 0:
        result += f'{days} day{"s" if days != 1 else ""}, '
    if hours > 0:
        result += f'{hours} hour{"s" if hours != 1 else ""}, '
    if minutes > 0:
        result += f'{minutes} minute{"s" if minutes != 1 else ""}, '
    if seconds > 0:
        result += f'{seconds} second{"s" if seconds != 1 else ""}'

    return result.rstrip(', ')