# bicycle

## 🧙‍♂️ DnD Character Sheet Manager

Сервис для управления листами персонажей Dungeons & Dragons.  
Позволяет создавать, хранить, редактировать и экспортировать листы персонажей в формате JSON.  
Поддерживает JWT-аутентификацию и разворачивается в Docker.

---

## 🚀 Функционал
- 📜 Создание, редактирование и удаление листов персонажей
- 🗄 Хранение данных в MongoDB
- 🔐 JWT-аутентификация
- 🌐 REST API (FastAPI)
- 📦 Полная контейнеризация (Docker + Docker Compose)

---

## 🛠 Технологии
- **Python 3.11**
- **FastAPI**
- **MongoDB** + **Motor**
- **JWT (PyJWT)**
- **Pydantic / pydantic-settings**
- **Docker, Docker Compose**

---

## 📂 Структура проекта
```
app/
│
├── main.py               # Точка входа
├── config.py             # Конфигурация проекта
├── db.py                 # Подключение к MongoDB
├── auth.py               # JWT-логика
├── models.py             # Pydantic-модели
├── sheets.py             # CRUD-операции с листами
└── routers/
    ├── auth_router.py    # Регистрация и логин
    └── sheets_router.py  # Листы персонажей
```

---

## ⚙️ Настройка окружения

Создайте файл `.env`:
```env
MONGO_URI=mongodb://mongo:27017
MONGO_DB=dnd
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Запуск через Docker
```bash
docker-compose up --build
```
После запуска API будет доступно по адресу:
```
http://localhost:8000
```
Swagger-документация:
```
http://localhost:8000/docs
```

---

## 🔑 Аутентификация (JWT)

### Регистрация
**POST** `/api/v1/auth/register`
```json
{
  "username": "player1",
  "password": "mypassword"
}
```

### Логин
**POST** `/api/v1/auth/login`
```json
{
  "username": "player1",
  "password": "mypassword"
}
```
**Ответ:**
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

Для всех защищённых маршрутов нужно передавать:
```http
Authorization: Bearer <jwt_token>
```

---

## 📜 Работа с листами персонажей

### Создать лист
**POST** `/api/v1/sheets`
```json
{
  "name": "Gorim Ironfist",
  "class": "Fighter",
  "level": 5,
  "stats": {
    "strength": 18,
    "dexterity": 12
  }
}
```

### Получить все листы
**GET** `/api/v1/sheets`

### Получить лист по ID
**GET** `/api/v1/sheets/{id}`

### Обновить лист
**PUT** `/api/v1/sheets/{id}`

### Удалить лист
**DELETE** `/api/v1/sheets/{id}`

---

## 📌 Планы на будущее
- 📱 Telegram-бот для работы с листами
- 📤 Экспорт в PDF/HTML
- 🎨 Web UI (React/Vue)
- 🔍 Поиск и фильтрация персонажей

---

## 📝 Лицензия
MIT
