import logging
from importlib import import_module

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from app.core.settings import settings
from app.core.database import engine
from app.core.static import static_files
from app.core.logging import config_logger
from app.core.security import CSRFMiddleware


config_logger(settings)
logger = logging.getLogger(__name__)


async def load_routes(app: Starlette):
    for feature_name in settings.app.features:
        try:
            feature_routes_module = import_module(f"app.features.{feature_name}.routes")
        except ModuleNotFoundError:
            pass
        else:
            routes = getattr(feature_routes_module, "routes", None)

            if routes is not None:
                app.routes.extend(routes)
        
        logger.info(f"loaded feature: {feature_name}")


async def create_tables():
    from app.features.users.models import Base
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)


async def lifespan(app: Starlette):
    await create_tables()
    await load_routes(app)
    yield
    logger.info("app finished.")


app = Starlette(
    debug=settings.app.debug,
    lifespan=lifespan,
    middleware=(
        Middleware(SessionMiddleware, secret_key=settings.app.secret_key, https_only=False),
        Middleware(CSRFMiddleware),
        # Middleware(AuthMiddleware),
        Middleware(CSRFProtectMiddleware, csrf_secret=settings.app.secret_key), 
    )
)


app.mount('/static', static_files, 'static')
