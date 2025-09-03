# ITSolutions TZ1 - Приложение для интеграции с Битрикс24

Веб-приложение Django для управления сделками через интеграцию с CRM Битрикс24.

## 🚀 Возможности

- **Интеграция с Битрикс24**: Полная интеграция через REST API
- **Управление сделками**: Просмотр, создание, редактирование сделок
- **Кастомные поля**: Автоматическое создание пользовательских полей в Битрикс24
- **Синхронизация**: Автоматическая синхронизация данных между приложением и Битрикс24
- **Фильтрация и поиск**: Продвинутые возможности фильтрации сделок
- **Современный UI**: Адаптивный интерфейс на Bootstrap 5

## 📋 Требования

- Python 3.8+
- PostgreSQL 12+
- Битрикс24 портал с доступом к REST API
- Django 4.2+

## 🛠 Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd ITSolutions/tz1
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

```sql
CREATE USER itsol_tz1 WITH PASSWORD 'password';
CREATE DATABASE itsol_tz1 OWNER itsol_tz1;
```

### 5. Настройка переменных окружения

Создайте файл `local_settings.py` на основе примера:

```python
# Локальные настройки для разработки
DEBUG = True
ALLOWED_HOSTS = ['*']

from integration_utils.bitrix24.local_settings_class import LocalSettingsClass

# Настройки приложения Битрикс24
APP_SETTINGS = LocalSettingsClass(
    portal_domain='your-portal.bitrix24.ru',  # Замените на ваш домен портала
    app_domain='localhost:8000',
    app_name='itsolutions_tz1',
    salt='your-salt-key-here-change-this',
    secret_key='your-secret-key-here-change-this',
    application_bitrix_client_id='your-client-id',
    application_bitrix_client_secret='your-client-secret',
    application_index_path='/',
)

# Настройки базы данных для разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'itsol_tz1',
        'USER': 'itsol_tz1',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запуск сервера разработки

```bash
python manage.py runserver
```

## 🔧 Настройка интеграции с Битрикс24

### 1. Создание приложения в Битрикс24

1. Перейдите в ваш портал Битрикс24
2. Откройте "Приложения" → "Другое" → "Создать приложение"
3. Выберите "Веб-приложение"
4. Заполните форму:
   - **Название**: ITSolutions TZ1
   - **Домен**: localhost:8000 (для разработки)
   - **URL приложения**: http://localhost:8000/
   - **Области**: CRM

### 2. Получение ключей доступа

После создания приложения вы получите:
- `CLIENT_ID` - идентификатор приложения
- `CLIENT_SECRET` - секретный ключ

### 3. Обновление настроек

Обновите `local_settings.py` с полученными ключами:

```python
APP_SETTINGS = LocalSettingsClass(
    portal_domain='your-portal.bitrix24.ru',
    app_domain='localhost:8000',
    app_name='itsolutions_tz1',
    salt='your-salt-key-here-change-this',
    secret_key='your-secret-key-here-change-this',
    application_bitrix_client_id='your-client-id',  # CLIENT_ID
    application_bitrix_client_secret='your-client-secret',  # CLIENT_SECRET
    application_index_path='/',
)
```

## 📱 Использование

### Главная страница

- Отображение информации о текущем пользователе Битрикс24
- Статистика по сделкам
- Последние 10 активных сделок
- Быстрые действия

### Управление сделками

- **Список сделок**: Просмотр всех сделок с фильтрацией
- **Создание сделки**: Форма создания новой сделки
- **Редактирование**: Изменение существующих сделок
- **Детальный просмотр**: Полная информация о сделке

### Кастомное поле "Приоритет сделки"

Приложение автоматически создает пользовательское поле в Битрикс24:
- **Тип**: Строка
- **Название**: "Приоритет сделки"
- **Значения**: Низкий, Средний, Высокий, Срочный
- **Возможности**: Фильтрация, отображение в списках

### Синхронизация

- Автоматическая синхронизация при входе
- Ручная синхронизация через интерфейс
- Логирование всех операций синхронизации

## 🏗 Архитектура

### Модели

- **Deal**: Основная модель сделки
- **DealSyncLog**: Логи синхронизации

### Сервисы

- **Bitrix24DealService**: Работа с API Битрикс24
- **DealService**: Локальная работа со сделками

### Представления

- **Dashboard**: Главная страница
- **DealsList**: Список сделок
- **DealForm**: Создание/редактирование сделок
- **UserProfile**: Профиль пользователя

## 🔒 Безопасность

- Аутентификация через Битрикс24
- CSRF защита
- Валидация всех входных данных
- Логирование операций

## 🚀 Развертывание

### Продакшн настройки

1. Обновите `local_settings.py`:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

2. Настройте статические файлы:
   ```bash
   python manage.py collectstatic
   ```

3. Настройте веб-сервер (Nginx + Gunicorn)

### Переменные окружения

```bash
export DJANGO_SETTINGS_MODULE=ITSolutionsTZ1.settings
export DATABASE_URL=postgresql://user:password@localhost/dbname
export BITRIX24_PORTAL_DOMAIN=your-portal.bitrix24.ru
export BITRIX24_CLIENT_ID=your-client-id
export BITRIX24_CLIENT_SECRET=your-client-secret
```

## 🧪 Тестирование

```bash
# Установка тестовых зависимостей
pip install -r requirements.txt

# Запуск тестов
python manage.py test

# Запуск с покрытием
coverage run --source='.' manage.py test
coverage report
```

## 📝 API Endpoints

### Основные URL

- `/` - Стартовая страница (интеграция с Битрикс24)
- `/app/` - Главная страница приложения
- `/app/deals/` - Список сделок
- `/app/deals/create/` - Создание сделки
- `/app/profile/` - Профиль пользователя
- `/app/sync/` - Синхронизация сделок

### REST API

Все API endpoints защищены аутентификацией Битрикс24.

## 🤝 Разработка

### Структура проекта

```
ITSolutionsTZ1/
├── main_app/           # Основное приложение
│   ├── models.py      # Модели данных
│   ├── views.py       # Представления
│   ├── forms.py       # Формы
│   ├── services.py    # Бизнес-логика
│   └── admin.py       # Админка
├── integration_utils/  # Утилиты интеграции
├── templates/         # HTML шаблоны
├── static/           # Статические файлы
└── manage.py         # Django управление
```

### Добавление новых полей

1. Обновите модель в `models.py`
2. Создайте миграцию: `python manage.py makemigrations`
3. Примените миграцию: `python manage.py migrate`
4. Обновите формы и представления

### Добавление новых API методов

1. Обновите `Bitrix24DealService`
2. Добавьте новые представления
3. Обновите URL маршруты
4. Добавьте тесты

## 📞 Поддержка

- **Документация**: [Ссылка на документацию]
- **Issues**: [GitHub Issues]
- **Email**: support@example.com

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.

## 🙏 Благодарности

- Команда Битрикс24 за отличное API
- Django Software Foundation
- Сообщество open source

---

**Версия**: 1.0.0  
**Дата**: 2024  
**Автор**: ITSolutions Team
