# User API

<p align="center">
  <a href="https://github.com/D1m7asis/UserHubAPI">
    <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  </a>
  <a href="https://github.com/D1m7asis/UserHubAPI/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </a>
  <a href="https://github.com/D1m7asis/UserHubAPI/actions">
    <img src="https://github.com/D1m7asis/UserHubAPI/actions/workflows/ci.yml/badge.svg" alt="Build Status">
  </a>
</p>

REST API для управления пользователями на базе LiteStar (Python 3.12) с CRUD-операциями для таблицы user в PostgreSQL.

## 📌 Технический стек
- **Backend**: LiteStar (версия 2.x)
- **База данных**: PostgreSQL + Advanced-SQLAlchemy
- **Инфраструктура**: Docker
- **Пакетный менеджер**: Poetry 1.8.3

## 🚀 Быстрый старт

### Предварительные требования
- Docker
- Docker Compose
- Python 3.12
- Poetry

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your_username/user-api.git
cd user-api
```

2. Установите зависимости:
```bash
poetry lock
poetry install
```

3. Запустите приложение через [docker-compose.yml](docker-compose.yml) (предпочтительно):

```bash
docker-compose up -d
```
(Либо же просто через Docker)
```bash
docker build -t myapp . && \
docker run -p 8000:8000 -e DATABASE_URL="postgresql+asyncpg://user:password@host.docker.internal:5432/users_db" myapp
```

#### 3.1. Дополнительно: 
Инициализируйте базу данных и таблицу users через [migrate.py](src/app/migrate.py), если это не произошло автоматически. 

## 📚 Документация API

После запуска сервера доступны следующие интерфейсы документации:

1. **Swagger UI**: http://localhost:8000/schema/swagger
2. **Redoc**: http://localhost:8000/schema/redoc
3. **Страница проверки задач**: http://localhost:8000/tasks

## 🗃️ Структура таблицы user

| Поле       | Тип данных               | Ограничения | Значение по умолчанию        |
|------------|--------------------------|-------------|------------------------------|
| id         | BIGINT                   | PRIMARY KEY | GENERATED ALWAYS AS IDENTITY |
| name       | VARCHAR(255)             | NOT NULL    | -                            |
| surname    | VARCHAR(255)             | NOT NULL    | -                            |
| password   | VARCHAR(255)             | NOT NULL    | -                            |
| created_at | TIMESTAMP WITH TIME ZONE | -           | (now() AT TIME ZONE 'UTC')   |
| updated_at | TIMESTAMP WITH TIME ZONE | -           | (now() AT TIME ZONE 'UTC')   |

## 🔍 Доступные endpoints
API поддерживает следующие операции:
- ✅ Создание пользователя (POST /users)
- ✅ Получение списка пользователей (GET /users)
- ✅ Получение данных одного пользователя (GET /users/{id})
- ✅ Обновление данных пользователя (PATCH /users/{id})
- ✅ Удаление пользователя (DELETE /users/{id})

## 🛠️ Техническое задание

### Цель
Создать REST API с CRUD-операциями для таблицы user.

### Требования
1. ✅ Поддержка Swagger/Redoc документации
2. ✅ Реализация всех CRUD операций
3. ✅ Валидация входных данных
4. ✅ Логирование операций
5. ✅ Конфигурация через переменные окружения

## ⏱️ Затраченное время
1 неделя

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
