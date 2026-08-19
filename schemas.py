from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    password: str
    email: EmailStr  # валидирует email сразу

class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True) # говорит pydantic брать данные из атрибутов ORM-объекта

class UserLogin(BaseModel):
    password: str
    email: EmailStr

class TokenCreate(BaseModel):
    id: int
    email: EmailStr
