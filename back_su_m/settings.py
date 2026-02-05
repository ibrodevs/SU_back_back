"""
Django settings for back_su_m project
с AWS S3 для хранения статики и медиа
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-change-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = [host.strip() for host in config('ALLOWED_HOSTS', default='*').split(',')]

# -------------------
# Logging
# -------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# -------------------
# Installed apps
# -------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',

    # Third party
    'rest_framework',
    'corsheaders',
    'django_filters',
    'mptt',
    'modeltranslation',

    # Local
    'news',
    'research',
    'careers',
    'banner',
    'teachers',
    'admissions',
    'hsm',
    'infrastructure',
    'documents',  # Добавляем новое приложение
    'student_life',  # Приложение студенческой жизни
    'media_coverage',  # Приложение медиа-покрытия
    'about_section',  # Секция "О нас" и партнеры
    'social_opportunities',  # Приложение социальных возможностей
    'mission_section.apps.MissionSectionConfig',  # Приложение секции миссии
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # можно убрать, если всё через S3
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'back_su_m.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'back_su_m.wsgi.application'

# -------------------
# Database
# -------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3"),
        conn_max_age=600,
        ssl_require=False,
    )
}

# -------------------
# Auth password validators
# -------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------
# Internationalization
# -------------------
LANGUAGES = [
    ('ru', 'Русский'),
    ('ky', 'Кыргызча'),
    ('en', 'English'),
]
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_LANGUAGES = ('ru', 'ky', 'en')
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'

# -------------------
# AWS S3 Storage (Bucketeer)
# -------------------
# Используем переменные от аддона Bucketeer
BUCKETEER_AWS_ACCESS_KEY_ID = config("BUCKETEER_AWS_ACCESS_KEY_ID", default=None)

if BUCKETEER_AWS_ACCESS_KEY_ID:
    # Bucketeer настройки
    AWS_ACCESS_KEY_ID = BUCKETEER_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = config("BUCKETEER_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("BUCKETEER_BUCKET_NAME")
    AWS_S3_REGION_NAME = config("BUCKETEER_AWS_REGION")
    AWS_QUERYSTRING_AUTH = False  # Публичные файлы не требуют подписи
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

    # Медиа файлы в папке public/ (публичный доступ)
    STORAGES = {
        "default": {  # медиа файлы в S3 в папке public/
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "public/media",  # Используем префикс public/
                "querystring_auth": False,  # Не требуем подписи для публичных файлов
            },
        },
        "staticfiles": {  # статика через WhiteNoise
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/public/media/"
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    # Локальное хранение для разработки
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# -------------------
# Django REST Framework
# -------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# -------------------
# CORS
# -------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://www.su-medical-school.com",
    "https://med-backend-d61c905599c2.herokuapp.com",
]

CORS_ALLOW_CREDENTIALS = True

# -------------------
# Email
# -------------------
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=0, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='no-reply@salymbekov.edu.kg')

ADMISSIONS_EMAIL_TO = config('ADMISSIONS_EMAIL_TO', default='adilhansatymkulov40@gmail.com')
STUDENT_APPEALS_EMAIL_TO = config('STUDENT_APPEALS_EMAIL_TO', default='adilhansatymkulov40@gmail.com')

# -------------------
# Default primary key field type
# -------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

