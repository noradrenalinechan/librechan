from pydantic import BaseModel

class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    username: str | None = None
    password: str | None = None

class Admin(AdminBase):
    id: int

    class Config:
        from_attributes = True