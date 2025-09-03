from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.conf import settings
import logging
from django.contrib import messages
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

@main_auth(on_cookies=True)
def start(request):
    """Главная страница для аутентифицированных пользователей"""
    try:
        # Создаем кастомное поле приоритета при авторизации пользователя
        if hasattr(request, 'bitrix_user_token') and request.bitrix_user_token:
            from main_app.services import Bitrix24Service
            service = Bitrix24Service(request.bitrix_user_token)
            
            # Сначала проверяем, существует ли уже поле
            try:
                response = request.bitrix_user_token.call_api_method('crm.deal.userfield.list', {})
                field_exists = False
                field_id = None
                if response.get('result'):
                    for field in response['result']:
                        if field.get('FIELD_NAME') == 'DEAL_PRIORITY':
                            field_exists = True
                            field_id = field.get('ID')
                            print(f"✅ Кастомное поле 'Приоритет сделки' найдено с ID: {field_id}")
                            
                            # Получаем детали поля для диагностики
                            try:
                                field_details = request.bitrix_user_token.call_api_method('crm.deal.userfield.get', {
                                    'id': field_id
                                })
                                print(f"🔍 Детали поля 'Приоритет сделки':")
                                print(f"   - ID: {field_details.get('result', {}).get('ID')}")
                                print(f"   - FIELD_NAME: {field_details.get('result', {}).get('FIELD_NAME')}")
                                print(f"   - USER_TYPE_ID: {field_details.get('result', {}).get('USER_TYPE_ID')}")
                                print(f"   - ENTITY_ID: {field_details.get('result', {}).get('ENTITY_ID')}")
                                print(f"   - LABEL: {field_details.get('result', {}).get('LABEL')}")
                                print(f"   - ACTIVE: {field_details.get('result', {}).get('ACTIVE')}")
                                print(f"   - SHOW_IN_LIST: {field_details.get('result', {}).get('SHOW_IN_LIST')}")
                                print(f"   - EDIT_IN_LIST: {field_details.get('result', {}).get('EDIT_IN_LIST')}")
                                
                                # Проверяем, правильно ли настроено поле
                                entity_id = field_details.get('result', {}).get('ENTITY_ID')
                                if entity_id != 'CRM_DEAL':
                                    print(f"⚠️ Поле привязано к неправильной сущности: {entity_id} (ожидалось CRM_DEAL)")
                                else:
                                    print("✅ Поле правильно привязано к сущности CRM_DEAL")
                                    
                            except Exception as e:
                                print(f"❌ Не удалось получить детали поля: {e}")
                            
                            break
                
                # Если поле не найдено, создаем его
                if not field_exists:
                    print("🆕 Создаем кастомное поле 'Приоритет сделки'...")
                    result = service.create_priority_field()
                    if result.get('success'):
                        print(f"✅ Кастомное поле 'Приоритет сделки' создано успешно! ID: {result.get('field_id')}")
                    else:
                        print(f"⚠️ Не удалось создать кастомное поле: {result.get('message')}")
                        
            except Exception as e:
                print(f"❌ Ошибка при проверке/создании кастомного поля: {e}")
                
    except Exception as e:
        print(f"❌ Ошибка при создании кастомного поля: {e}")
    
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


@main_auth(on_cookies=True)
def recreate_priority_field(request):
    """Удаляет и создает заново кастомное поле приоритета"""
    try:
        if hasattr(request, 'bitrix_user_token') and request.bitrix_user_token:
            from main_app.services import Bitrix24Service
            service = Bitrix24Service(request.bitrix_user_token)
            
            print("🔄 Начинаем пересоздание поля приоритета...")
            
            # 1. Удаляем существующее поле
            print("🗑️ Удаляем существующее поле...")
            delete_result = service.delete_priority_field()
            
            if delete_result.get('success'):
                print("✅ Поле успешно удалено")
                
                # 2. Создаем поле заново
                print("🆕 Создаем поле заново...")
                create_result = service.create_priority_field()
                
                if create_result.get('success'):
                    print("✅ Поле успешно создано заново!")
                    messages.success(request, 'Поле приоритета успешно пересоздано!')
                else:
                    print(f"❌ Ошибка при создании поля: {create_result.get('message')}")
                    messages.error(request, f'Ошибка при создании поля: {create_result.get("message")}')
            else:
                print(f"❌ Ошибка при удалении поля: {delete_result.get('message')}")
                messages.error(request, f'Ошибка при удалении поля: {delete_result.get("message")}')
                
        else:
            messages.error(request, 'Не удалось получить токен для работы с API')
            
    except Exception as e:
        print(f"❌ Ошибка при пересоздании поля: {e}")
        messages.error(request, f'Ошибка при пересоздании поля: {str(e)}')
    
    # Перенаправляем обратно на главную
    return redirect('start:home')
