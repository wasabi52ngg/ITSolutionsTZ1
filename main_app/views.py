from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from .forms import DealForm
from .services import Bitrix24Service


@main_auth(on_cookies=True)
def deals_list(request):
    """Список всех сделок пользователя"""
    try:
        user = request.bitrix_user
        user_token = request.bitrix_user_token
        
        bitrix_service = Bitrix24Service(user_token)
        deals = bitrix_service.get_user_deals(limit=10)
        
        context = {
            'deals': deals,
            'user': user,
        }
        
        return render(request, 'main_app/deals_list.html', context)
        
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке сделок: {str(e)}')
        return render(request, 'main_app/error.html', {'error': str(e)})


@method_decorator(main_auth(on_cookies=True), name='dispatch')
class DealCreateView(View):
    """Представление для создания новой сделки"""
    template_name = 'main_app/deal_form.html'
    success_url = reverse_lazy('main_app:deals_list')
    
    def get(self, request):
        """Отображение формы"""
        form = DealForm()
        context = {
            'form': form,
            'user': request.bitrix_user,
            'action': 'create'
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Обработка отправки формы"""
        form = DealForm(request.POST)
        
        if form.is_valid():
            try:
                user_token = request.bitrix_user_token
                bitrix_service = Bitrix24Service(user_token)
                
                deal_data = form.cleaned_data
                result = bitrix_service.create_deal(deal_data)
                
                if result.get('success'):
                    messages.success(request, 'Сделка успешно создана в Битрикс24!')
                    return redirect(self.success_url)
                else:
                    messages.error(request, result.get('message', 'Ошибка при создании сделки'))
                    
            except Exception as e:
                messages.error(request, f'Ошибка при создании сделки: {str(e)}')
        
        # Если форма невалидна или произошла ошибка, показываем форму снова
        context = {
            'form': form,
            'user': request.bitrix_user,
            'action': 'create'
        }
        return render(request, self.template_name, context)
