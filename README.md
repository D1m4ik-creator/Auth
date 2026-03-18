# Auth API (Django + DRF + JWT)

Небольшой API для регистрации, входа и выхода пользователя с JWT-токенами.

## Быстрый старт

1. Создай и активируй виртуальное окружение:

```
git clone https://github.com/D1m4ik-creator/Auth.git
```

```
python -m venv .venv
.\.venv\Scripts\activate
```

2. Установи зависимости:

```powershell
pip install -r requirements.txt
```

3. Примени миграции:

```powershell
python auth\manage.py makemigrations
python auth\manage.py migrate
```

4. Запусти сервер:

```powershell
python auth\manage.py runserver
```

## Документация API

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
