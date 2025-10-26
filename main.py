from fastapi import FastAPI
from app.api.insert_endpoint import insert_router
from app.api.research_endpoint import router_research

app = FastAPI()
app.include_router(insert_router, prefix="/api/v1")
app.include_router(router_research, prefix="/api/v1")