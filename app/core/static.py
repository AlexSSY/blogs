from starlette.staticfiles import StaticFiles

from app.core.settings import BASE_DIR


static_files = StaticFiles(directory=BASE_DIR / 'static')
