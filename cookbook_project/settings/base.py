import os
from pathlib import Path

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.contrib.messages import constants as messages

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "cloudinary",
    "cookbook",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cookbook_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"]
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cookbook_project.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "uk-ua"

TIME_ZONE = "Europe/Kyiv"

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = "cookbook.User"


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUD_NAME"),
    'API_KEY': os.getenv("API_KEY"),
    'API_SECRET': os.getenv("API_SECRET"),
}


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "cloudinary_storage.storage.StaticCloudinaryStorage",
    },
}

STATICFILES_STORAGE = "cloudinary_storage.storage.StaticCloudinaryStorage"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


LOGIN_REDIRECT_URL = "cookbook:index"
LOGOUT_REDIRECT_URL = "cookbook:index"
LOGIN_URL = "accounts:login"


MESSAGE_TAGS = {
    messages.ERROR: "danger",
}
