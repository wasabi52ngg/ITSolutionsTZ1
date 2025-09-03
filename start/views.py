from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.conf import settings

@main_auth(on_cookies=True)
def start(request):
    """Главная страница для аутентифицированных пользователей"""
    app_settings = settings.APP_SETTINGS
    return render(request, 'start_page.html', locals())

def home(request):
    """Простая главная страница для всех пользователей"""
    try:
        # Пытаемся получить пользователя, если он аутентифицирован
        if hasattr(request, 'bitrix_user') and request.bitrix_user:
            user = request.bitrix_user
            context = {
                'user': user,
                'is_authenticated': True
            }
        else:
            context = {
                'user': None,
                'is_authenticated': False
            }
        
        return render(request, 'start_page.html', context)
    except:
        # Если что-то пошло не так, показываем страницу без пользователя
        return render(request, 'start_page.html', {
            'user': None,
            'is_authenticated': False
        })
