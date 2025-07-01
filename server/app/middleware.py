from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [r"https?:\/\/localhost:\d{4}"]


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
    )
