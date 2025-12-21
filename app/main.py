import logging

from starlette.applications import Starlette

from app.core.settings import settings
from app.routes.blogs import routes as base_routers


logger = logging.getLogger(__name__)


app = Starlette(
    debug=settings.app.debug,
    routes=base_routers
)
