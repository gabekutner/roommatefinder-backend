from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr


class User(Document):
  fname:str
  lname:str
  email:EmailStr
  password:str

  class Config:
    json_schema_extra = {
      "example": {
        "fname": "Gabe",
        "lname": "Kutner",
        "email": "gabe@hotmail.dev",
        "password": "12345",
      }
    }
  
  class Settings:
    name = "user"

class UserSignIn(HTTPBasicCredentials):
  class Config:
    json_schema_extra = {
      "example": {"email": "gabe@hotmail.dev", "password": "12345"},
    }