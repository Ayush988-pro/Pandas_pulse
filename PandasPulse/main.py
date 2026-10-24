from fastapi import FastAPI
from Databases.db import  engine
from Models.user import Base
from Routers.users import router
from Models.dataset import Dataset
from Routers.datasets import router as dataset_router
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)
app.include_router(dataset_router)