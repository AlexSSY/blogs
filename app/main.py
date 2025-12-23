import logging

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from app.core.settings import settings
from app.routes.blogs import routes as base_routers
from app.models.blogs import create_tables
from app.core.static import static_files
from app.core.logging import config_logger


config_logger(settings)
logger = logging.getLogger(__name__)


async def lifespan(app: Starlette):
    await create_tables()
    yield


app = Starlette(
    debug=settings.app.debug,
    routes=base_routers,
    lifespan=lifespan,
    middleware=(
        Middleware(SessionMiddleware, secret_key=settings.app.secret_key, https_only=False), 
        Middleware(CSRFProtectMiddleware, csrf_secret=settings.app.secret_key), 
    )
)

app.mount('/', static_files, 'static')
