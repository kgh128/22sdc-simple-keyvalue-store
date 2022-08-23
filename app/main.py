from fastapi import FastAPI
from utils.appExceptions import AppExceptionCase, app_exception_handler

store = dict()
app = FastAPI()

@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)
@app.get("/")
async def root():
    return {"message": "Hello World"}