from starlette.templating import Jinja2Templates

from app.core.settings import BASE_DIR


class Templating:
    def __init__(self, *dirs: str):
        dirs = list(map(lambda dir: BASE_DIR / dir, dirs))
        self.templating = Jinja2Templates(dirs)


templating = Jinja2Templates("templates")
