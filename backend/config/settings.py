from pathlib import Path
from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage
from datetime import timedelta




from . import docs_schema


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=True)
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # MARK: THIRD-PARTY APPS
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "djoser",
    "storages",
    # MARK: INTERNAL APPS
    "apps.roles",
    "apps.store",
    "apps.comment",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # MARK: CUSTOM MIDDLEWARES
    "middleware.anon_req_handler.StrangerRequestHandler",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DB = config("DB", default="slqlit", cast=str)

match DB:
    case "PSQL":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("DB_NAME"),
                "USER": config("DB_USER"),
                "PASSWORD": config("DB_PASS"),
                "HOST": config("DB_HOST"),
                "PORT": config("DB_PORT"),
            }
        }

    case _:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

S3_FILE_UPLOAD_MAX_MEMORY_SIZE = 0

WSGI_APPLICATION = "config.wsgi.application"

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

LANGUAGE_CODE = "Tehran-Asia"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [BASE_DIR / 'static',]
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'uploads'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "roles.BaseUser"

# MARK: THIRD-PARTY PACKAGES CONFIGURATION
SPECTACULAR_SETTINGS = docs_schema.SPECTACULAR_SETTINGS


class Liara(S3Boto3Storage):
    def __init__(self, **settings):
        super().__init__(**settings)

        self.bucket_name = config("S3_BUCKET")
        self.endpoint_url = config("S3_ENDPOINT")
        self.access_key = config("S3_ACCESS_KEY")
        self.secret_key = config("S3_SECRET_KEY")
        self.querystring_auth = False
        self.default_acl = "public-read"
LIARA_STORAGE = Liara 

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=2),
}

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

DJOSER = {
    # 'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': '#/activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    "SERIALIZERS": {
        "user_create": "apps.roles.serializers.CustomerCreateSerializer",
        "current_user": "apps.roles.serializers.CustomerSerializer",
    },
}
