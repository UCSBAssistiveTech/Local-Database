from fastapi import FastAPI
from app.rds.db import engine
import app.rds.models as models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
# app.include_router(api.routes.router)

