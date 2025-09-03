from django import forms
from django.utils import timezone


class DealForm(forms.Form):
    """Простая форма для создания сделки"""
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название сделки'
        }),
        label="Название сделки"
    )
    
    opportunity = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        label="Сумма сделки"
    )
    
    currency_id = forms.ChoiceField(
        choices=[('RUB', 'Рубль'), ('USD', 'Доллар'), ('EUR', 'Евро')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Валюта"
    )
    
    probability = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '100'}),
        label="Вероятность (%)"
    )
    
    begin_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date(),
        label="Дата начала"
    )
    
    close_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=(timezone.now() + timezone.timedelta(days=7)).date(),
        label="Дата закрытия"
    )
    
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите комментарии к сделке'}),
        required=False,
        label="Комментарии"
    )
    
    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        begin_date = cleaned_data.get('begin_date')
        close_date = cleaned_data.get('close_date')
        
        if begin_date and close_date and begin_date > close_date:
            raise forms.ValidationError(
                "Дата начала не может быть позже даты закрытия"
            )
        
        return cleaned_data
