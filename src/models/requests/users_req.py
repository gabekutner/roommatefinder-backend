from typing import Optional
from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
  fname:str
  lname:str
  email:EmailStr

  class Config:
    json_schema_extra = {
      "example": {
        "fname": "Gabe",
        "lname": "Kutner",
        "email": "gabe@hotmail.dev"
      }
    }

class UpdateUserReq(BaseModel):
  fname: Optional[str] = None
  lname: Optional[str] = None
  email: Optional[EmailStr] = None

  class Collection:
    name = "user"

  class Config:
    json_schema_extra = {
      "example": {
        "fname": "Joe",
        "lname": "Shmo",
        "email": "shmo@hotmail.deves"
      }
    }