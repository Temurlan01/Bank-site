# Bank Site

Учебное банковское веб-приложение на Django с REST API, регистрацией и аутентификацией пользователей.

## Что это

Проект моделирует базовый пользовательский сценарий банковского сервиса:

- регистрация и управление пользователями;
- авторизация через JWT;
- OAuth/social login;
- взаимодействие с банковским API;
- административная часть и документация API;
- CORS для подключения frontend-клиента.

## Зачем

Pet-проект создан для практики backend-разработки на Django: проектирования API, работы с JWT и OAuth, разделения приложения на доменные модули и построения основы для финансового кабинета.

## Стек

- **Python 3.9+**
- **Django 5.2**
- **Django REST Framework 3.16**
- **Simple JWT** — access/refresh tokens
- **social-auth-app-django / OAuth** — социальная авторизация
- **drf-yasg** — Swagger/OpenAPI
- **django-cors-headers** — CORS
- **Pillow** — работа с изображениями
- **SQLite** — база данных для локальной разработки

## Быстрый старт

```bash
git clone https://github.com/Temurlan01/Bank-site.git
cd Bank-site
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Приложение будет доступно по адресу http://127.0.0.1:8000.

> Для OAuth-провайдеров и production рекомендуется задать client ID/secret и секретный ключ через переменные окружения. Не храните реальные credentials в репозитории.

## Скриншоты и демо

Публичный demo URL не настроен. Для презентации можно добавить в `docs/screenshots/` скриншоты регистрации, входа, личного кабинета и Swagger UI:

```md
![Авторизация](docs/screenshots/auth.png)
![Личный кабинет](docs/screenshots/dashboard.png)
![API documentation](docs/screenshots/swagger.png)
```

## Структура

```text
bank/          # основное банковское приложение
bank_project/  # настройки Django и маршрутизация
users/         # пользователи и аутентификация
static/        # статические файлы
manage.py      # CLI Django
```

## Статус

Проект предназначен для локального запуска и дальнейшего расширения: операции со счетами, переводы, история транзакций и production-развёртывание.

## Лицензия

Лицензия пока не указана.
