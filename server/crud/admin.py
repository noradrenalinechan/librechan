from sqlalchemy.orm import Session
from server.models.admin import Admin
from server.schemas.admin import AdminCreate, AdminUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_admin_by_id(db: Session, admin_id: int):
    """Получить администратора по ID."""
    return db.query(Admin).filter(Admin.id == admin_id).first()

def get_admin_by_username(db: Session, username: str):
    """Получить администратора по имени пользователя."""
    return db.query(Admin).filter(Admin.username == username).first()

def get_all_admins(db: Session, skip: int = 0, limit: int = 100):
    """Получить список всех администраторов с пагинацией."""
    return db.query(Admin).offset(skip).limit(limit).all()

def create_admin(db: Session, admin: AdminCreate):
    hashed_password = pwd_context.hash(admin.password)  # Хэшируем пароль
    db_admin = Admin(username=admin.username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin: AdminUpdate):
    """Обновить данные администратора."""
    db_admin = get_admin_by_id(db, admin_id)
    if not db_admin:
        return None

    if admin.username:
        db_admin.username = admin.username
    if admin.password:
        db_admin.hashed_password = pwd_context.hash(admin.password)  # Хэшируем новый пароль

    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    """Удалить администратора."""
    db_admin = get_admin_by_id(db, admin_id)
    if not db_admin:
        return None

    db.delete(db_admin)
    db.commit()
    return db_admin

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)