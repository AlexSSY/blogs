import os, sys
from starlette.templating import Jinja2Templates

from app.core.settings import settings, BASE_DIR


class Templating:
    def __init__(self, *dirs: str):
        dirs = list(map(lambda dir: BASE_DIR / dir, dirs))
        self.templating = Jinja2Templates(dirs)

FEATURES_DIR = BASE_DIR / "features"

features_templates_directories = [
    FEATURES_DIR / d / settings.app.templates_dir for d in settings.app.features
]

def filter_for_existing_dirs(template_directory):
    return os.path.exists(template_directory) and os.path.isdir(template_directory)


features_templates_directories = list(
    filter(filter_for_existing_dirs, features_templates_directories)
)

templating = Jinja2Templates(features_templates_directories)
