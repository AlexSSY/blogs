import logging
from importlib import import_module

from app.core.settings import settings


from logging import getLogger


logger = getLogger(__name__)


class Features:
    def __init__(self):
        self.features = list()

    async def load_features(self):
        for feature_name in settings.app.features:
            feature_module = import_module(f"app.{feature_name}")
            self.features.append(feature_module)
            logger.info(f"Feature: {feature_name} loaded!")


features = Features()
