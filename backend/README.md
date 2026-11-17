# ФинСмарт — Backend API (FastAPI)

Асинхронный REST API сервис интеллектуальной платформы личных финансов «ФинСмарт».

## Архитектура проекта

Проект построен по принципам **трехзвенной слоистой архитектуры (Layered Architecture)** с разделением ответственности:

```text
HTTP Request (Frontend)
       │
       ▼
1. API Router (app/api/v1/)        — Прием запросов, Pydantic валидация, HTTP статус-коды
       │
       ▼
2. Services (app/services/)        — Чистая бизнес-логика (расчет балансов, 50/30/20, хеширование)
       │
       ▼
3. Repositories (app/repositories/)— Слой доступа к данным (SQLAlchemy Async, CRUD)
       │
       ▼
SQLite / PostgreSQL Database
```

## Стек технологий

- **Фреймворк:** Python 3.10+ / FastAPI (полностью асинхронный)
- **База данных:** SQLite (локально) с поддержкой асинхронности (`aiosqlite`) и совместимостью с PostgreSQL через SQLAlchemy 2.0
- **Безопасность:** Хэширование паролей через `bcrypt`, аутентификация через JWT-токены (`pyjwt`)
- **Валидация данных:** Pydantic v2 (строгая типизация с `Decimal` для финансовых сумм)
- **Документация:** OpenAPI / Swagger UI (автогенерация)

---

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск сервера разработки
```bash
uvicorn main:app --reload --port 8000
```

Сервер запустится по адресу: `http://127.0.0.1:8000`

### 3. Интерактивная документация (Swagger UI)
Откройте в браузере:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## Основные эндпоинты API (`/api/v1`)

### Аутентификация
- `POST /api/v1/auth/register` — Регистрация нового пользователя (логин, пароль, имя)
- `POST /api/v1/auth/login` — Вход в систему (возвращает JWT токен)
- `GET /api/v1/auth/me` — Получение данных текущего пользователя

### Операции (Транзакции)
- `GET /api/v1/transactions` — Список операций с фильтрацией по категории и типу (`expense`/`income`)
- `POST /api/v1/transactions` — Добавление операции (автоматически обновляет баланс)
- `GET /api/v1/transactions/summary` — Сводка для верхних карточек дашборда (баланс, доходы, расходы, сбережения)

### Категории
- `GET /api/v1/categories` — Список категорий с месячными лимитами и цветами
- `POST /api/v1/categories` — Создание новой персональной категории

### Цели и копилки
- `GET /api/v1/goals` — Список целей с расчетом процента накопления
- `POST /api/v1/goals` — Создание финансовой цели
- `POST /api/v1/goals/{id}/deposit` — Пополнение цели (списывает с баланса)

### Аналитика
- `GET /api/v1/analytics/categories` — Доли расходов по категориям для круговой диаграммы
- `GET /api/v1/analytics/rule-50-30-20` — Расчет пропорций по гарвардскому правилу 50/30/20

---

## Памятка для фронтенд-разработчика (JavaScript fetch)

Для вызова защищенных эндпоинтов передавайте полученный при логине токен в заголовке `Authorization`:

```javascript
// Пример получения операций
const token = localStorage.getItem('access_token');

const response = await fetch('http://127.0.0.1:8000/api/v1/transactions', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const transactions = await response.json();
```
