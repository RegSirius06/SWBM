import re

from django import template
from django.utils.safestring import mark_safe, SafeText

register = template.Library()

@register.filter
def format_text(text: str) -> SafeText:
    formatted_text = text

    formatted_text = re.sub(r'<<(.*?)>>', r'<blockquote class="blockquote text-dark p-3" style="background: #EEEEEE;"><small>\1</small></blockquote>', formatted_text)
    formatted_text = re.sub(r'__(.*?)__', r'<u>\1</u>', formatted_text)
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_text)
    formatted_text = re.sub(r'_(.*?)_', r'<i>\1</i>', formatted_text)
    formatted_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_text)
    formatted_text = re.sub(r'!~!(.*?)!~!', r'<mark>\1</mark>', formatted_text)
    formatted_text = re.sub(r'~~(.*?)~~', r'<s>\1</s>', formatted_text)
    formatted_text = re.sub(r'-!-(.*?)-!-', r'<small>\1</small>', formatted_text)

    return mark_safe(formatted_text)