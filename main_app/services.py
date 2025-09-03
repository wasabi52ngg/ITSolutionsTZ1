import logging
from typing import List, Dict, Any

from integration_utils.bitrix24.models import BitrixUserToken

logger = logging.getLogger(__name__)


class Bitrix24Service:
    """Простой сервис для работы с API Битрикс24"""
    
    def __init__(self, user_token: BitrixUserToken):
        self.user_token = user_token
    
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
                    'PROBABILITY', 'BEGINDATE', 'CLOSEDATE', 'DATE_CREATE'
                ],
                'order': {'DATE_CREATE': 'DESC'},
                'start': 0
            })
            
            if response.get('result'):
                return response['result'][:limit]
            
            return []
            
        except Exception as e:
            logger.error(f"Ошибка при получении сделок: {e}")
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
