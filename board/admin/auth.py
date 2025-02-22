from fastapi import Request, HTTPException
from sqladmin.authentication import AuthenticationBackend
from board.crud.admin import get_admin_by_username, verify_password
from board.database.database import SessionLocal

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        db = SessionLocal()
        admin = get_admin_by_username(db, username)
        db.close()

        if not admin or not verify_password(password, admin.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        request.session.update({"token": "admin"})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == "admin"