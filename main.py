from fastapi import FastAPI
from routers import users, products, auth_users, usersdb
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers de la API
app.include_router(users.router) 
app.include_router(products.router)
app.include_router(auth_users.router)
app.include_router(usersdb.router)

#Rutas estaticas de la API
app.mount("/statics", StaticFiles(directory="static"), name="static")

# Definiendo rutas de la API con FastAPI
@app.get("/")
async def root():
    return "hola mundo"

@app.get("/helloworld")
async def json():
    return {"message": "Hello World"}
