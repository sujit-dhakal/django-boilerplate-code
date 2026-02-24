from decouple import config

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

STATIC_URL = config("STATIC_URL", default="/static/")

STATIC_ROOT = BASE_DIR / "static"
STATIC_DIRS = [
    BASE_DIR / "static",
]

MEDIA_ROOT = "media/"
MEDIA_URL = "/media/"
