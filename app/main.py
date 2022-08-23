from fastapi import FastAPI

store = dict()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}