from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
from .database import SessionLocal, engine
from . import new_models
from .base_api_view import router
new_models.Base.metadata.create_all(bind=engine)
# from main import app
app = FastAPI()

# router = APIRouter(prefix='/items')
app.include_router(router)