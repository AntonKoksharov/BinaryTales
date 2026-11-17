import asyncio
import sys
from httpx import AsyncClient, ASGITransport
from main import app
from app.db.session import init_db

async def run_tests():
    print("Инициализация таблиц БД...", flush=True)
    await init_db()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        print("1. Тест ping...", flush=True)
        resp = await client.get("/api/v1/ping")
        assert resp.status_code == 200, f"Ping failed: {resp.text}"
        print("-> OK:", resp.json(), flush=True)

        print("2. Тест регистрации пользователя...", flush=True)
        register_payload = {
            "username": "alex01",
            "password": "secret_password_123",
            "full_name": "Александр"
        }
        resp = await client.post("/api/v1/auth/register", json=register_payload)
        assert resp.status_code in [201, 409], f"Register failed: {resp.text}"
        print("-> Register OK:", resp.status_code, flush=True)

        print("3. Тест авторизации (login)...", flush=True)
        login_payload = {
            "username": "alex01",
            "password": "secret_password_123"
        }
        resp = await client.post("/api/v1/auth/login", json=login_payload)
        assert resp.status_code == 200, f"Login failed: {resp.text}"
        data = resp.json()
        token = data["access_token"]
        assert token, "Token not found"
        print("-> Login OK! Получен JWT токен.", flush=True)

        headers = {"Authorization": f"Bearer {token}"}

        print("4. Тест получения профиля /api/v1/auth/me...", flush=True)
        resp = await client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 200
        user_info = resp.json()
        print(f"-> Профиль: {user_info['username']} | Баланс: {user_info['balance']}", flush=True)

        print("5. Тест получения категорий...", flush=True)
        resp = await client.get("/api/v1/categories", headers=headers)
        assert resp.status_code == 200
        cats = resp.json()
        assert len(cats) >= 8
        print(f"-> Категории: успешно получено {len(cats)} категорий", flush=True)

        cat_id = cats[0]["id"]

        print("6. Тест добавления транзакции...", flush=True)
        tx_payload = {
            "amount": 1540.0,
            "type": "expense",
            "category_id": cat_id,
            "description": "Супермаркет Перекресток"
        }
        resp = await client.post("/api/v1/transactions", json=tx_payload, headers=headers)
        assert resp.status_code == 201
        tx_data = resp.json()
        print(f"-> Транзакция создана: {tx_data['description']} - {tx_data['amount']} ₽", flush=True)

        print("7. Тест сводки дашборда...", flush=True)
        resp = await client.get("/api/v1/transactions/summary", headers=headers)
        assert resp.status_code == 200
        summary = resp.json()
        print("-> Сводка дашборда:", summary, flush=True)

        print("8. Тест создания цели (копилки)...", flush=True)
        goal_payload = {
            "title": "На новый ноутбук",
            "target_amount": 150000.0,
            "current_amount": 60000.0,
            "monthly_payment": 12500.0
        }
        resp = await client.post("/api/v1/goals", json=goal_payload, headers=headers)
        assert resp.status_code == 201
        goal_data = resp.json()
        print(f"-> Цель создана: {goal_data['title']}, прогресс: {goal_data['progress_percent']}%", flush=True)

        print("\n ВСЕ ТЕСТЫ БЭКЕНДА УСПЕШНО ПРОЙДЕНЫ! ", flush=True)

if __name__ == "__main__":
    asyncio.run(run_tests())
