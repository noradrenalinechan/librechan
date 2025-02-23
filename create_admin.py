import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Импортируйте модель администратора и Base из вашего проекта
from board.models.admin import Admin
from board.database.database import Base

# Настройки подключения к базе данных (используйте ваши настройки)
ENV = os.getenv("ENV", "docker")

if ENV == "local":
    from server.database.config_local import *
else:
    from server.database.config_docker import *

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Инициализация CryptContext для хэширования паролей
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_admin(username: str, password: str):
    """Создает администратора с хэшированным паролем и добавляет его в базу данных."""
    # Хэширование пароля
    hashed_password = pwd_context.hash(password)

    # Создание объекта администратора
    admin = Admin(username=username, hashed_password=hashed_password)

    # Подключение к базе данных
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    # Добавление администратора в базу данных
    with Session(engine) as session:
        # Проверяем, существует ли администратор с таким именем
        existing_admin = session.query(Admin).filter(Admin.username == username).first()
        if existing_admin:
            print(f"Администратор с именем '{username}' уже существует.")
            return

        session.add(admin)
        session.commit()
        print(f"Администратор '{username}' успешно создан.")

if __name__ == "__main__":
    # Фиксированные имя и пароль администратора
    username = "admin"
    password = "admin"

    # Создание администратора
    create_admin(username, password)