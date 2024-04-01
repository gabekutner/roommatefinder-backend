from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from beanie import PydanticObjectId

from repository.users_repo import UserRepo
from models.data import users
from models.requests import users_req


router = APIRouter()


@router.get("/users")
async def get_users():
  """ List all users. """
  repo: UserRepo = UserRepo()
  users = await repo.get_users()
  return JSONResponse(content=jsonable_encoder(users), status_code=200)


@router.get("/users/{id}")
async def get_user(id: PydanticObjectId):
  """ Get user by id. """
  repo: UserRepo = UserRepo()
  user = await repo.get_user(id)
  return JSONResponse(content=jsonable_encoder(user), status_code=200)


@router.post("/users")
async def add_user(user: users.User = Body(...)):
  """ Add a user. """
  repo: UserRepo = UserRepo()
  new_user = await repo.add_user(user)
  return JSONResponse(content=jsonable_encoder(new_user), status_code=200)


@router.put("/users/{id}")
async def update_user(id: PydanticObjectId, req: users_req.UpdateUserReq = Body(...)):
  """ Update a user. """
  repo: UserRepo = UserRepo()
  user = await repo.update_user(id, req.dict(exclude_unset=True))
  if update_user:
    return JSONResponse(content=jsonable_encoder(user), status_code=200)
  else:
    return JSONResponse(content={"message": f"Error updating user with id: {id}"}, status_code=404)
  

@router.delete("/users/{id}")
async def delete_user(id: PydanticObjectId):
  """ Delete a user. """
  repo: UserRepo = UserRepo()
  user = await repo.delete_user(id)
  if user:
    return JSONResponse(content=jsonable_encoder(user), status_code=200)
  else:
    return JSONResponse(content={"message": f"Error deleting user with id: {id}"}, status_code=404)