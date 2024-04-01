import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from configuration.db_config import init_database
from controllers import users


app = FastAPI()

main_app_lifespan = app.router.lifespan_context

@asynccontextmanager
async def lifespan(app):
  async with main_app_lifespan(app) as maybe_state:
    await init_database()
    yield

app.router.lifespan_context = lifespan

@app.get("/", tags=["Root"])
async def read_root():
  return {"message": "Welcome to roommatefinder.com."}

app.include_router(users.router, tags=["Users"])


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)