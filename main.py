from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import api_router
from config.database import Base, engine

app = FastAPI(title="API de Laudos Psicológicos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router,prefix="/api/v1")
Base.metada.create_all(bind=engine)