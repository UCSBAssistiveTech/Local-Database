from fastapi import FastAPI
from rds.db import engine
import routers.rds
import rds.models as models

import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(routers.rds.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)