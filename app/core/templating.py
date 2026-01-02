import os
from starlette.templating import Jinja2Templates

from app.core.settings import settings, BASE_DIR


FEATURES_DIR = BASE_DIR / "features"

features_templates_directories = [
    FEATURES_DIR / d / settings.app.templates_dir for d in settings.app.features
]

def by_existing_dirs(template_directory):
    return os.path.exists(template_directory) and os.path.isdir(template_directory)

features_templates_directories = list(
    filter(by_existing_dirs, features_templates_directories)
)

templates_directories = [BASE_DIR / "core/templates"] + \
            features_templates_directories

templating = Jinja2Templates(templates_directories)
