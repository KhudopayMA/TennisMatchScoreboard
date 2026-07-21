# Проект “Табло теннисного матча”

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Django Version](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/download/)

## Веб-приложение, реализующее табло счёта теннисного матча.
### Возможности пользователя:
- Создание матча
- Добавление очков игрокам в матче
- Просмотр списка матчей

### Используемые технологии:

- BACKEND - python 3.12
- web framework - Django 5
- WSGI HTTP - gunicorn
- database - mysql 9.7
- test - pytest
- FRONTEND:
    - HTML5
    - CSS3
    - Bootstrap 5
    - JavaScript
- CI - GitHub actions
- web server - nginx
- deploy - docker, docker-compose

### Deploy

1. Клонируйте репазиторий:
```bash
git clone https://github.com/KhudopayMA/TennisMatchScoreboard.git
cd TennisMatchScoreboard
```
2. Создайте .env файл. В файле .env.example указаны необходимые настройки для запуска проекта.
3. Запускаете через docker:
```bash
docker compose up -d
```

