from .base import *


SECRET_KEY = "django-insecure-)&zsu0tm2t6#5^d5*3&q6l8r@^7$u#qflb2kp3zclc)rplaiqp"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


