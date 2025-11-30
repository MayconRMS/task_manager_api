from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    name: str
    email: str
    password: constr(min_length=6, max_length=72) 

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str
