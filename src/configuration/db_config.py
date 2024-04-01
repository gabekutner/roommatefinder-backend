from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from models.data import users


class Settings(BaseSettings):
  # database configurations
  DATABASE_URL: Optional[str] = None

  class Config:
    env_file = ".env"
    from_attributes = True


async def init_database():
  client = AsyncIOMotorClient(Settings().DATABASE_URL)
  await init_beanie(database=client.get_default_database(), document_models=[users.User])