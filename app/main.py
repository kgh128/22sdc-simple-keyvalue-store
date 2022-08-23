from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.appExceptions import AppExceptionCase, app_exception_handler
from utils.requestExceptions import (http_exception_handler, request_validation_exception_handler, )

store = dict()
app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.get("/")
async def root():
    return {"message": "Hello World"}
