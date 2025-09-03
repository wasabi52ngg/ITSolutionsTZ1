import logging
from typing import List, Dict, Any

from integration_utils.bitrix24.models import BitrixUserToken

logger = logging.getLogger(__name__)


class Bitrix24Service:
    """Простой сервис для работы с API Битрикс24"""
    
    def __init__(self, user_token: BitrixUserToken):
        self.user_token = user_token
    
    def delete_priority_field(self) -> Dict[str, Any]:
        """Удаляет кастомное поле 'Приоритет сделки'"""
        try:
            # Сначала находим ID поля
            response = self.user_token.call_api_method('crm.deal.userfield.list', {})
            field_id = None
            if response.get('result'):
                for field in response['result']:
                    if field.get('FIELD_NAME') == 'UF_CRM_DEAL_PRIORITY':
                        field_id = field.get('ID')
                        break
            
            if field_id:
                # Удаляем поле
                delete_response = self.user_token.call_api_method('crm.deal.userfield.delete', {
                    'id': field_id
                })
                
                if delete_response.get('result'):
                    print(f"✅ Кастомное поле 'Приоритет сделки' удалено с ID: {field_id}")
                    return {'success': True, 'message': 'Поле удалено успешно'}
                else:
                    return {'success': False, 'message': 'Ошибка при удалении поля'}
            else:
                return {'success': False, 'message': 'Поле не найдено'}
                
        except Exception as e:
            print(f"❌ Ошибка при удалении кастомного поля: {e}")
            return {'success': False, 'message': str(e)}

    def create_priority_field(self) -> Dict[str, Any]:
        """Создает кастомное поле 'Приоритет сделки' используя call_api_method"""
        try:
            # Создаем кастомное поле типа enumeration (список)
            response = self.user_token.call_api_method('crm.deal.userfield.add', {
                'fields': {
                    'USER_TYPE_ID': 'enumeration',
                    'FIELD_NAME': 'DEAL_PRIORITY',
                    'LABEL': 'Приоритет сделки',
                    'LIST_FILTER_LABEL': 'Приоритет сделки',
                    'LIST_COLUMN_LABEL': 'Приоритет',
                    'EDIT_FORM_LABEL': 'Приоритет сделки',
                    'HELP_MESSAGE': 'Выберите приоритет для данной сделки',
                    'MANDATORY': 'Y',  # Обязательное поле
                    'SHOW_FILTER': 'Y',  # Показывать в фильтре
                    'SHOW_IN_LIST': 'Y',  # Показывать в списке
                    'EDIT_IN_LIST': 'Y',  # Разрешить редактирование в списке
                    'SORT': 500,
                    'LIST': [
                        {'VALUE': 'Высокий', 'SORT': 100, 'DEF': 'N', 'XML_ID': '3'},
                        {'VALUE': 'Средний', 'SORT': 200, 'DEF': 'Y', 'XML_ID': '2'},
                        {'VALUE': 'Низкий', 'SORT': 300, 'DEF': 'N', 'XML_ID': '1'}
                    ]
                }
            })
            
            if response.get('result'):
                logger.info(f"Кастомное поле 'Приоритет сделки' создано с ID: {response['result']}")
                return {
                    'success': True,
                    'field_id': response['result'],
                    'message': 'Кастомное поле создано успешно',
                    'already_exists': False
                }
            
            return {'success': False, 'message': 'Ошибка при создании кастомного поля'}
            
        except Exception as e:
            logger.error(f"Ошибка при создании кастомного поля: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_user_deals(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получает последние активные сделки пользователя"""
        try:
            response = self.user_token.call_api_method('crm.deal.list', {
                'filter': {
                    'ASSIGNED_BY_ID': self.user_token.user.bitrix_id,
                    'CLOSED': 'N'  # Только активные сделки
                },
                'select': [
                    'ID', 'TITLE', 'OPPORTUNITY', 'CURRENCY_ID', 
                    'PROBABILITY', 'BEGINDATE', 'CLOSEDATE', 'DATE_CREATE',
                    'UF_CRM_DEAL_PRIORITY'  # Кастомное поле приоритета
                ],
                'order': {'DATE_CREATE': 'DESC'},
                'start': 0
            })
            
            if response.get('result'):
                deals = response['result'][:limit]
                
                # Обрабатываем значения приоритета
                for deal in deals:
                    print(deal)
                    priority_value = deal.get('UF_CRM_DEAL_PRIORITY')
                    print(f"🔍 Сделка {deal.get('ID')}: значение приоритета = {priority_value} (тип: {type(priority_value)})")
                    
                    if priority_value is not None and priority_value != '':
                        # Преобразуем числовое значение в строковое
                        if str(priority_value) == '1':
                            deal['UF_CRM_DEAL_PRIORITY'] = 'low'
                            print(f"  ✅ преобразовано в 'low' (Низкий)")
                        elif str(priority_value) == '2':
                            deal['UF_CRM_DEAL_PRIORITY'] = 'medium'
                            print(f"  ✅ преобразовано в 'medium' (Средний)")
                        elif str(priority_value) == '3':
                            deal['UF_CRM_DEAL_PRIORITY'] = 'high'
                            print(f"  ✅ преобразовано в 'high' (Высокий)")
                        elif str(priority_value) == '0':
                            print(f"  ❓ значение 0, устанавливаем None")
                            # Значение 0 означает неправильно созданное поле
                            deal['UF_CRM_DEAL_PRIORITY'] = None
                    else:
                        print(f"  ❌ значение отсутствует")
                
                return deals
            
            return []
            
        except Exception as e:
            print(f"❌ Ошибка при получении сделок: {e}")
            return []
    
    def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создает новую сделку в Битрикс24"""
        try:
            fields = {
                'TITLE': deal_data['title'],
                'OPPORTUNITY': float(deal_data['opportunity']),
                'CURRENCY_ID': deal_data['currency_id'],
                'PROBABILITY': int(deal_data['probability']),
                'BEGINDATE': deal_data['begin_date'].strftime('%Y-%m-%d'),
                'CLOSEDATE': deal_data['close_date'].strftime('%Y-%m-%d'),
                'COMMENTS': deal_data.get('comments', ''),
                'ASSIGNED_BY_ID': self.user_token.user.bitrix_id,
                'UF_CRM_DEAL_PRIORITY' : deal_data['priority']
            }
            
            response = self.user_token.call_api_method('crm.deal.add', {
                'fields': fields
            })
            
            if response.get('result'):
                return {
                    'success': True,
                    'deal_id': response['result'],
                    'message': 'Сделка успешно создана'
                }
            
            return {'success': False, 'message': 'Ошибка при создании сделки'}
            
        except Exception as e:
            logger.error(f"Ошибка при создании сделки: {e}")
            return {'success': False, 'message': str(e)}
