from fastapi.routing import APIRoute
from app.config.settings import settings
from app.middleware import make_middleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.cors.exception.base import CustomException
from app.api import router

def on_auth_error(_request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

def create_app()-> FastAPI:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_DEFAULT_VERSION,
        openapi_url=f"{settings.api_base_path}/openapi.json",
        description="wedding table seating chart",
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
        generate_unique_id_function=custom_generate_unique_id,
        middleware=make_middleware()
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_

app = create_app()

def main():
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
