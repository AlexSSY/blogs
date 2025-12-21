import logging

from starlette.applications import Starlette

from app.core.settings import settings
from app.routes.blogs import routes as base_routers
from app.models.blogs import create_tables
from app.core.static import static_files


logger = logging.getLogger(__name__)


async def lifespan(app: Starlette):
    await create_tables()
    yield


app = Starlette(
    debug=settings.app.debug,
    routes=base_routers,
    lifespan=lifespan
)

app.mount('/', static_files, 'static')
