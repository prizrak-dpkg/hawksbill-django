from .base_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = []


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "****",
        "USER": "****",
        "PASSWORD": "********",
        "HOST": "********",
        "PORT": 3306,
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# Channel layers
# https://pypi.org/project/channels-redis/

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "PASSWORD": "********",
        "CONFIG": {
            "hosts": [("redis://:********@127.0.0.1:6379/0")],
        },
    },
}


# Token expiration
# Variable that stores the seconds counted after the creation date to make the token expire.

EXPIRATION_SECONDS: float = 900.0


# CORS Settings
# https://pypi.org/project/django-cors-headers/

CORS_ALLOWED = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOWED_ORIGINS = [*CORS_ALLOWED]

CORS_ORIGIN_WHITELIST = [*CORS_ALLOWED]


# drf-yasg
# https://drf-yasg.readthedocs.io/en/stable/settings.html

SWAGGER_SETTINGS = {
    "DOC_EXPANSION": "none",
}


# CKEditor configuration
# https://django-ckeditor.readthedocs.io/en/latest/#optional-customizing-ckeditor-editor

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"


# Media files (Files uploaded by the user)
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"
