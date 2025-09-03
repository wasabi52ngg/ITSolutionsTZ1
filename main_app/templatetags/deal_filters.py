from django import template
from django.utils import timezone
from datetime import datetime
import re

register = template.Library()


@register.filter
def format_bitrix_date(value):
    """Форматирует дату из Битрикс24 в читаемый вид"""
    if not value:
        return "Не указана"
    
    try:
        if isinstance(value, str):
            if '+' in value:
                value = value.split('+')[0]
            elif 'T' in value:
                pass
            else:
                return value
        
        if 'T' in str(value):
            dt = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(str(value))
        
        if dt.hour == 0 and dt.minute == 0:
            return dt.strftime('%d.%m.%Y')
        else:
            return dt.strftime('%d.%m.%Y %H:%M')
            
    except (ValueError, TypeError):
        return str(value)


@register.filter
def format_comments(value, max_length=50):
    """Форматирует комментарии, обрезая длинный текст"""
    if not value:
        return "Нет комментариев"
    
    clean_text = re.sub(r'<[^>]+>', '', str(value))
    
    clean_text = ' '.join(clean_text.split())
    
    if len(clean_text) <= max_length:
        return clean_text
    
    return clean_text[:max_length] + "..."
