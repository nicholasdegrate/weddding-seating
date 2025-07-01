import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from .config.settings import settings
from .middleware import register_middleware
from app.api.monitoring import monitoring_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_DEFAULT_VERSION,
    openapi_url=f"{settings.api_base_path}/openapi.json",
    description="wedding table seating chart",
    generate_unique_id_function=custom_generate_unique_id,
)

register_middleware(app)


def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


app.include_router(monitoring_router, prefix=settings.api_base_path)

if __name__ == "__main__":
    main()
