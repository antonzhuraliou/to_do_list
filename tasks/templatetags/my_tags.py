from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def correct_cancel(context):
    which_edit = context.get('which_edit')
    query = context.get('query')
    date = context.get('date')
    if which_edit == 'History':
        link = reverse('tasks:history')
    elif which_edit == 'History_search':
        link = reverse('tasks:search') + f'?query={query}'
    elif which_edit == 'Task':
        link = reverse('tasks:main_page')
    elif which_edit == 'Calendar_last':
        link = reverse('calendar_tasks:day_task', kwargs={'day': date.day, 'month': date.month, 'year':date.year})
    else:
        link = reverse('calendar_tasks:completed_task', kwargs= {'day': date.day, 'month': date.month, 'year':date.year})
    return mark_safe(link)