from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse

from starlette.middleware.sessions import SessionMiddleware

from app.exceptions import handler_uncaught_exception, invalid_data, InvalidData, incorrect_configuration
from app.routers.users import users_api_router
from app.routers.record import record_api_router
from app.settings import get_settings

SETTINGS = get_settings()


# def get_swagger_ui_html_custom(*, openapi_url: str, title: str) -> str:
#     return get_swagger_ui_html(
#         openapi_url=openapi_url,
#         title=title,
#         swagger_js_url="/static/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui.css",
#     )


def init_app():
    _app = FastAPI(redoc_url=None,
                   docs_url=None,
                   title='HealthTechInnovations',
                   debug=SETTINGS.debug,
                   openapi_url="/docs/openapi.json")

    _app.include_router(users_api_router)
    _app.include_router(record_api_router)

    _app.add_middleware(SessionMiddleware, https_only=SETTINGS.https_only, secret_key=SETTINGS.secret_key,
                        same_site="strict")

    _app.add_exception_handler(InvalidData, invalid_data)
    _app.add_exception_handler(RequestValidationError, incorrect_configuration)
    _app.add_exception_handler(Exception, handler_uncaught_exception)

    return _app


app = init_app()


@app.get("/docs", response_class=HTMLResponse)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title)


@app.get("/redoc", response_class=HTMLResponse)
async def redoc_html():
    return get_redoc_html(openapi_url=app.openapi_url, title=app.title)
