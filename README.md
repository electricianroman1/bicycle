# Bicycle LSS Project

Поддержка листов персонажей из **Long Story Short**: API принимает и сохраняет JSON **как есть** в поле `payload`. Имя персонажа автоматически извлекается из `payload.data.name.value` (поддерживается, даже если `data` — строка JSON).

## Быстрый старт
```bash
docker compose up --build
```

Сервисы:
- API: http://localhost:8000 (Swagger: http://localhost:8000/docs)
- Mongo Express: http://localhost:8081 (логин/пароль: admin/admin)
- MongoDB: mongodb://localhost:27017 (БД по умолчанию: dnd)

## API
Базовый префикс: `/api/v1`

**Создать лист из LSS JSON**
```
POST /api/v1/sheets
Authorization: Bearer demo
Content-Type: application/json

{
  "payload": { ... LSS JSON ... }
}
```

**Список листов**
```
GET /api/v1/sheets
Authorization: Bearer demo
```

**Получить по id**
```
GET /api/v1/sheets/{id}
Authorization: Bearer demo
```

**Обновить**
```
PATCH /api/v1/sheets/{id}
Authorization: Bearer demo

{
  "payload": { ... LSS JSON ... }
}
```

**Удалить**
```
DELETE /api/v1/sheets/{id}
Authorization: Bearer demo
```

> Примечание по аутентификации: для простоты используется заглушка — любой непустой Bearer-токен считается валидным, а имя пользователя — `demo`.

## Импорт файла напрямую в Mongo
```
python tools/import_lss_json.py "Уэллби Мертвослав — Long Story Short (1).json"
# или в контейнере:
docker compose exec backend python /app/tools/import_lss_json.py /app/Уэллби.json
```
Переменная `IMPORT_OWNER` задаёт владельца записи (по умолчанию `demo`).
