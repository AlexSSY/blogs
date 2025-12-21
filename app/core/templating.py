from starlette.templating import Jinja2Templates

from app.core.settings import settings, BASE_DIR


templating = Jinja2Templates(
    BASE_DIR / settings.app.templates_dir
)