from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from board.database.database import get_db
from board.crud.admin import (
    get_admin_by_id,
    get_all_admins,
    create_admin,
    update_admin,
    delete_admin, get_admin_by_username,
)
from board.schemas.admin import AdminCreate, AdminUpdate, Admin

router = APIRouter()

@router.post("/admins/", response_model=Admin)
def create_new_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Создать нового администратора."""
    db_admin = get_admin_by_username(db, username=admin.username)
    if db_admin:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_admin(db=db, admin=admin)

@router.get("/admins/", response_model=list[Admin])
def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех администраторов."""
    admins = get_all_admins(db, skip=skip, limit=limit)
    return admins

@router.get("/admins/{admin_id}", response_model=Admin)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    """Получить администратора по ID."""
    db_admin = get_admin_by_id(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.put("/admins/{admin_id}", response_model=Admin)
def update_existing_admin(admin_id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    """Обновить данные администратора."""
    db_admin = get_admin_by_id(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return update_admin(db=db, admin_id=admin_id, admin=admin)

@router.delete("/admins/{admin_id}", response_model=Admin)
def delete_existing_admin(admin_id: int, db: Session = Depends(get_db)):
    """Удалить администратора."""
    db_admin = get_admin_by_id(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return delete_admin(db=db, admin_id=admin_id)