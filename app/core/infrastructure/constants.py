import os

from core.infrastructure.settings import environment_settings

ENVIRONMENT = os.getenv("ENVIRONMENT")

SETTINGS = environment_settings.get(ENVIRONMENT)
