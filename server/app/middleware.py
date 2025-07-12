from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from typing import List

origins = [r"https?:\/\/localhost:\d{4}"]

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


