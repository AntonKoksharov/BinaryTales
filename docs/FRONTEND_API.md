# 🚀 Памятка по интеграции API ФинСмарт для Фронтенд-разработчика

Привет! Бэкенд на **FastAPI** с базой данных **SQLite** готов, настроен и запушен в репозиторий в ветку `main`.

---

## 📥 1. Подготовка и запуск бэкенда у себя

Сделай в терминале проекта:
```bash
git pull
```

Затем запусти сервер:
```bash
cd backend
pip install -r requirements.txt
py -m uvicorn main:app --reload
```

* 🟢 **Сервер запустится по адресу:** `http://127.0.0.1:8000`
* 📖 **Интерактивная документация Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  > В Swagger можно тестировать любые запросы прямо из браузера через кнопку **«Try it out»**.

---

## 🔑 2. Базовый URL и Авторизация

* **Базовый URL:** `http://127.0.0.1:8000/api/v1`
* **CORS:** Полностью настроен (`*`), запросы с `localhost:5173` (Vite) или `localhost:5500` блокироваться не будут.
* **Токен:** Все защищенные эндпоинты требуют заголовок:
  ```http
  Authorization: Bearer <твой_токен_из_localStorage>
  ```

---

## 📡 3. Таблица основных эндпоинтов

| Метод | Эндпоинт | Назначение | Тело запроса / Параметры |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Регистрация нового аккаунта | `{"username", "password", "full_name"}` |
| `POST` | `/auth/login` | Вход и получение токена | `{"username", "password"}` |
| `GET` | `/auth/me` | Данные текущего пользователя | *(Bearer токен)* |
| `GET` | `/transactions/summary` | Сводка для верхних карточек дашборда | Отдает: баланс, доходы, расходы, сбережения |
| `GET` | `/transactions` | Список всех операций | `?limit=50&category_id=1&type=expense` |
| `POST` | `/transactions` | Добавление новой операции | `{"amount", "type", "category_id", "description"}` |
| `GET` | `/categories` | Список категорий расходов | Отдает: названия, цвета (`#HEX`), лимиты |
| `GET` | `/goals` | Список финансовых целей (копилок) | Отдает: цели и рассчитанный `%` прогресса |
| `POST` | `/goals/{id}/deposit` | Пополнение копилки | `{"amount": 5000}` (списывает с баланса) |
| `GET` | `/analytics/categories` | Данные для круговой диаграммы | Суммы и проценты трат по категориям |
| `GET` | `/analytics/rule-50-30-20`| Гарвардское правило 50 / 30 / 20 | Фактические и целевые суммы |

---

## 💻 4. Готовые примеры на JavaScript (`fetch`)

Ты можешь сразу вставить эти функции в `main.js`:

### 1. Авторизация (Вход)
```javascript
const API_URL = 'http://127.0.0.1:8000/api/v1';

async function login(username, password) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка авторизации');
    }

    // Сохраняем токен в браузере
    localStorage.setItem('access_token', data.access_token);
    console.log('Успешный вход! Пользователь:', data.user);
    return data.user;
  } catch (error) {
    alert(error.message);
  }
}
```

### 2. Загрузка данных для верхних карточек Дашборда
```javascript
async function loadDashboardStats() {
  const token = localStorage.getItem('access_token');
  if (!token) return console.warn('Пользователь не авторизован');

  const response = await fetch(`${API_URL}/transactions/summary`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  const stats = await response.json();
  console.log('Сводка:', stats);

  // Пример подстановки в верстку:
  // document.querySelector('.stat-card:nth-child(1) .stat-value').textContent = `${stats.total_balance} ₽`;
  // document.querySelector('.stat-card:nth-child(2) .stat-value').textContent = `+${stats.total_income} ₽`;
  // document.querySelector('.stat-card:nth-child(3) .stat-value').textContent = `${stats.total_expense} ₽`;
  // document.querySelector('.stat-card:nth-child(4) .stat-value').textContent = `${stats.saved_amount} ₽`;
}
```

### 3. Добавление новой траты
```javascript
async function addExpense(amount, categoryId, description) {
  const token = localStorage.getItem('access_token');

  const response = await fetch(`${API_URL}/transactions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      amount: parseFloat(amount),
      type: 'expense',
      category_id: categoryId,
      description: description
    })
  });

  const result = await response.json();
  console.log('Транзакция успешно добавлена:', result);
  // Баланс пользователя на бэкенде пересчитался автоматически!
}
```
