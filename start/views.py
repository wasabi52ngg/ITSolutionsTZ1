from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@main_auth(on_cookies=True)
def start(request):
    """Главная страница для аутентифицированных пользователей"""
    try:
        if hasattr(request, 'bitrix_user_token') and request.bitrix_user_token:
            from main_app.services import Bitrix24Service
            service = Bitrix24Service(request.bitrix_user_token)

            try:
                response = request.bitrix_user_token.call_api_method('crm.deal.userfield.list', {})
                field_exists = False
                field_id = None
                if response.get('result'):
                    for field in response['result']:
                        if field.get('FIELD_NAME') == 'DEAL_PRIORITY':
                            field_exists = True
                            field_id = field.get('ID')

                            try:
                                field_details = request.bitrix_user_token.call_api_method('crm.deal.userfield.get', {
                                    'id': field_id
                                })

                            except Exception as e:
                                print(f"Не удалось получить детали поля: {e}")

                            break

                if not field_exists:
                    result = service.create_priority_field()
                    if result.get('success'):
                        print(f"Кастомное поле 'Приоритет сделки' создано успешно! ID: {result.get('field_id')}")
                    else:
                        print(f"Не удалось создать кастомное поле: {result.get('message')}")

            except Exception as e:
                print(f"Ошибка при проверке/создании кастомного поля: {e}")

    except Exception as e:
        print(f"Ошибка при создании кастомного поля: {e}")

    app_settings = settings.APP_SETTINGS
    context = {
        'user': request.bitrix_user,
        'is_authenticated': True,
        'app_settings': app_settings
    }
    return render(request, 'start_page.html', context)


@main_auth(on_cookies=True)
def home(request):
    """Простая главная страница для всех пользователей"""
    context = {
        'user': request.bitrix_user,
        'is_authenticated': True
    }
    return render(request, 'start_page.html', context)
