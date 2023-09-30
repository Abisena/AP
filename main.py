from fastapi import FastAPI
from ecomerce_api import Auth, Crud

app = FastAPI()

@app.get('/')
async def Start():
    return {
        "status": 200,
        "message": "OK",
    }

app.include_router(Auth.app, tags=['AUTH'], prefix='/Auth')

app.include_router(Crud.crud, tags=['CRUD'], prefix='/Crud')