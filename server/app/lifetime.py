from contextlib import asynccontextmanager
from typing import Awaitable, Callable, AsyncGenerator
from fastapi import FastAPI

from app.config.settings import init_firebase_admin_app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_firebase_admin_app()

    yield
    # TODO: change to logging system
    print("FastAPI is shutting down")
