from fastapi import FastAPI
import app.core.config
from app.api.endpoints import router as v1_router

app = FastAPI()
app.include_router(v1_router, prefix="/api/v1")