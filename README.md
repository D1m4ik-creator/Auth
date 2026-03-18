# Auth API (Django + DRF + SimpleJWT)

Небольшой API для регистрации и JWT-аутентификации.

## Быстрый старт

1. Клонирование и переход в проект:

```bash
git clone https://github.com/D1m4ik-creator/Auth.git
cd Auth_API
```

2. Виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. Установка зависимостей:

```powershell
pip install -r auth\requirements.txt
```

4. Миграции:

```powershell
python auth\manage.py makemigrations
python auth\manage.py migrate
```

5. Запуск:

```powershell
python auth\manage.py runserver --noreload
```

## Документация API

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## JWT

Используются только стандартные роуты `SimpleJWT`:

- `POST /api/token/`
- `POST /api/token/refresh/`
- `POST /api/token/verify/`

Важно: в этом проекте логин пользователя - это `email` (модель `User` с `USERNAME_FIELD = 'email'`).

### 1) Получить access + refresh

`POST /api/token/`

```json
{
  "email": "alex@example.com",
  "password": "StrongPass123!"
}
```

Ответ:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### 2) Ходить в защищенные эндпоинты

Передавать заголовок:

```http
Authorization: Bearer <access_token>
```

### 3) Обновить access

Когда access истекает, вызвать:

`POST /api/token/refresh/`

```json
{
  "refresh": "<refresh_token>"
}
```

Ответ:

```json
{
  "access": "<new_access_token>"
}
```

### 4) Проверить токен

`POST /api/token/verify/`

```json
{
  "token": "<access_or_refresh_token>"
}
```

## Как фронту работать с токенами

1. При входе получить пару токенов через `/api/token/`.
2. `access` добавлять в `Authorization` для защищенных запросов.
3. На `401` пробовать `/api/token/refresh/` и повторять исходный запрос.
4. При выходе очищать токены на фронте.

## Остальные эндпоинты проекта

- `POST /api/register/` - регистрация пользователя
- `POST /api/login/` - кастомный login (можно не использовать, если работаешь по дефолтному SimpleJWT)
- `POST /api/logout/` - кастомный logout с blacklist refresh
