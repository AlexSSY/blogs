import logging

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from app.core.settings import settings
from app.core.database import engine
from app.core.static import static_files
from app.core.logging import config_logger


config_logger(settings)
logger = logging.getLogger(__name__)


async def lifespan(app: Starlette):
    from app.features.users.models import Base
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
    yield


def application_routes() -> tuple[Route]:
    from app.features.blog.routes import routes as blog_routes
    from app.features.auth.routes import routes as auth_routes
    return auth_routes + blog_routes


app = Starlette(
    debug=settings.app.debug,
    routes=application_routes(),
    lifespan=lifespan,
    middleware=(
        Middleware(SessionMiddleware, secret_key=settings.app.secret_key, https_only=False),
        # Middleware(AuthMiddleware),
        Middleware(CSRFProtectMiddleware, csrf_secret=settings.app.secret_key), 
    )
)

app.mount('/', static_files, 'static')
