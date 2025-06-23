import uvicorn
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [r"https?:\/\/localhost:\d{4}"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)


@app.get("/ping")
def ping():
    return {"message": "pong"}


def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
