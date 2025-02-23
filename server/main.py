import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from server.admin.auth import AdminAuth
from server.admin.views import PostAdmin, CommentAdmin, AdminView
from server.routes import post, comment, admin_router
from server.database.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key="secret"))

admin.add_view(PostAdmin)
admin.add_view(CommentAdmin)
admin.add_view(AdminView)

app.include_router(post.router, prefix="/api")
app.include_router(comment.router, prefix="/api")
app.include_router(admin_router.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)