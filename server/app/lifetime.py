from contextlib import asynccontextmanager
from typing import Awaitable, Callable, AsyncGenerator
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    # TODO: change to logging system
    print("FastAPI is shutting down")
