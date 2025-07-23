from fastapi import APIRouter


table_router = APIRouter()


@table_router.post("/")
async def create_table():
    pass
