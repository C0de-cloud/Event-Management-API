# Event Management API

API для системы регистрации и управления мероприятиями.

## Функциональность

- Регистрация и авторизация пользователей
- Создание и управление мероприятиями
- Регистрация участников на мероприятия
- Категории мероприятий
- Места проведения мероприятий
- Отзывы и рейтинги
- Поиск и фильтрация мероприятий

## Технический стек

- Python 3.10+
- FastAPI 0.95+
- MongoDB (через Motor для асинхронной работы)
- Pydantic 2.0+
- JWT для аутентификации

## Установка и запуск

1. Клонировать репозиторий
2. Создать виртуальное окружение:
   ```
   python -m venv venv
   source venv/bin/activate  # для Linux/macOS
   venv\Scripts\activate     # для Windows
   ```
3. Установить зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Создать файл `.env` на основе `.env.example`
5. Запустить MongoDB
6. Запустить приложение:
   ```
   python main.py
   ```

После запуска API будет доступно по адресу http://localhost:8000

## API Endpoints

### Аутентификация

- `POST /api/auth/register` - Регистрация нового пользователя
- `POST /api/auth/login` - Авторизация и получение JWT токена
- `POST /api/auth/refresh-token` - Обновление JWT токена

### Пользователи

- `GET /api/users/me` - Получение информации о текущем пользователе
- `PUT /api/users/me` - Обновление информации о текущем пользователе
- `GET /api/users/{user_id}` - Получение информации о пользователе

### Мероприятия

- `POST /api/events` - Создание нового мероприятия
- `GET /api/events` - Получение списка мероприятий с фильтрацией
- `GET /api/events/{event_id}` - Получение мероприятия по ID
- `PUT /api/events/{event_id}` - Обновление мероприятия
- `DELETE /api/events/{event_id}` - Удаление мероприятия
- `GET /api/events/categories` - Получение списка категорий мероприятий

### Участие в мероприятиях

- `POST /api/events/{event_id}/register` - Регистрация на мероприятие
- `DELETE /api/events/{event_id}/register` - Отмена регистрации на мероприятие
- `GET /api/events/{event_id}/attendees` - Получение списка участников мероприятия
- `GET /api/users/me/events` - Получение списка мероприятий пользователя

### Места проведения

- `POST /api/venues` - Создание нового места проведения
- `GET /api/venues` - Получение списка мест проведения
- `GET /api/venues/{venue_id}` - Получение места проведения по ID
- `PUT /api/venues/{venue_id}` - Обновление места проведения
- `DELETE /api/venues/{venue_id}` - Удаление места проведения

### Отзывы

- `POST /api/events/{event_id}/reviews` - Добавление отзыва о мероприятии
- `GET /api/events/{event_id}/reviews` - Получение отзывов о мероприятии
- `PUT /api/reviews/{review_id}` - Обновление отзыва
- `DELETE /api/reviews/{review_id}` - Удаление отзыва

## Роли пользователей

- **USER** - базовые права: регистрация на мероприятия, добавление отзывов
- **ORGANIZER** - создание и управление собственными мероприятиями
- **ADMIN** - полные права: управление всеми мероприятиями, пользователями и местами проведения

## Примеры запросов

### Создание мероприятия

```
POST /api/events
{
  "title": "Конференция по технологиям",
  "description": "Описание конференции...",
  "start_date": "2023-12-01T10:00:00",
  "end_date": "2023-12-01T18:00:00",
  "category_id": "category_id_here",
  "venue_id": "venue_id_here",
  "max_attendees": 100,
  "price": 1500,
  "is_private": false
}
```

### Регистрация на мероприятие

```
POST /api/events/{event_id}/register
```

### Добавление отзыва

```
POST /api/events/{event_id}/reviews
{
  "rating": 5,
  "comment": "Отличное мероприятие!"
}
```
