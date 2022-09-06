import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.s3Storage import s3_connection
from app.routers import item

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


app.include_router(item.router)


@app.get("/")
async def root():
    return PlainTextResponse(str("Simple Key-Value Store"))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
