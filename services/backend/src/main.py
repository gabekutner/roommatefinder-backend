""" main.py """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:8000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def get_root():
  """ home """
  return {"message": "home directory"}