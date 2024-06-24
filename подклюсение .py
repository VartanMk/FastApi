from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/mydatabase"

engine = create_engine(DB_URL)

try:
    connection = engine.connect()
    print("Подключение установлено")
    connection.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")
