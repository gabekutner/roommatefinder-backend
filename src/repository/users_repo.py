from typing import List, Union

from beanie import PydanticObjectId

from models.data.users import User


class UserRepo:
  """ User Repository """
  def __init__(self):
    self.user_collection = User
  
  async def add_user(self, new_user: User) -> User:
    user = await new_user.create()
    return user

  async def get_users(self) -> List[User]:
    users = await self.user_collection.all().to_list()
    return users

  async def get_user(self, id: PydanticObjectId) -> User:
    user = await self.user_collection.get(id)
    if user:
      return user
    
  async def update_user(self, id: PydanticObjectId, data: dict) -> Union[bool, User]:
    update_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in update_body.items()}}
    user = await self.user_collection.get(id)
    if user:
      await user.update(update_query)
      return user
    return False

  async def delete_user(self, id: PydanticObjectId) -> bool:
    user = await self.user_collection.get(id)
    if user:
      await user.delete()
      return True