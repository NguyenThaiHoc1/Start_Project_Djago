"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import ast
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta


env_file = os.environ.get('CADOCR_SERVER_ENV_FILE', '.env_dev')
print(f'CadOcr Server use env_file: {env_file}')
load_dotenv(
    find_dotenv(env_file),
    override=False,
)

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/catalog/example'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get(
    'CADOCR_SERVER_SECRETKEY',
    'InsecureKeyForDevelopmentUseOnly-88PLBYau9I0qgHq5ZQuoMLrU1fiC78bu',
)

DEBUG = os.environ.get('CADOCR_SERVER_APPDEBUG', 'true').lower() == 'true'


ALLOWED_HOSTS = {
    'localhost', '127.0.0.1',
}
CADOCR_SERVER_ADDRESS = os.environ.get('CADOCR_SERVER_ADDRESS', None)
if CADOCR_SERVER_ADDRESS:
    ALLOWED_HOSTS.add(CADOCR_SERVER_ADDRESS)
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
CORS_ALLOWED_ORIGIN_REGEXES = [
    f'^http(s?)://{allowed_host}'
    for allowed_host in ALLOWED_HOSTS
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',

    # Our Webapp
    'catalog',

    # Health check
    'health_check',
    'health_check.db',
    'health_check.contrib.migrations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

ASGI_APPLICATION = 'config.asgi.application'
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

USE_PG_DB = os.environ.get('CADOCR_DB_USE_PG_DB', 'true').lower() == 'true'
if USE_PG_DB:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Normal postgreSQL
        # 'ENGINE': 'timescale.db.backends.postgis',  # TimescaleDB support
        'NAME': os.environ.get('CADOCR_DB_DBNAME', 'cadocr'),
        'USER': os.environ.get('CADOCR_DB_USER', 'cadocr'),
        'PASSWORD': os.environ.get('CADOCR_DB_PASSWORD', 'Abc12345'),
        'HOST': os.environ.get('CADOCR_DB_HOST', 'localhost'),
        'PORT': os.environ.get('CADOCR_DB_PORT', '5432'),
    }
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DB_BATCH_SIZE = ast.literal_eval(
    os.environ.get('CADOCR_DB_BATCH_SIZE', '800')
)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'user_number',
    # 'USER_ID_CLAIM': 'user_number',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

use_cache = os.environ.get('CADOCR_CACHE_USE_CACHE', 'true').lower() == 'true'
if use_cache:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': f'{os.environ.get("CADOCR_CACHE_HOST")}:{os.environ.get("CADOCR_CACHE_PORT")}',
        }
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_HOST = os.environ.get('CADOCR_EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = ast.literal_eval(os.environ.get('CADOCR_EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('CADOCR_EMAIL_USER', 'yourmail@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('CADOCR_EMAIL_PASSWORD', 'gmail-password')
EMAIL_FROM_EMAIL = os.environ.get('CADOCR_EMAIL_FROMEMAIL', 'yourmail@gmail.com')
EMAIL_USE_TLS = os.environ.get('CADOCR_EMAIL_USETLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('CADOCR_EMAIL_USESSL', 'True').lower() == 'true'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

enable_log_file = os.environ.get('CADOCR_SERVER_ENABLE_LOG_FILE', 'false').lower() == 'true'
LOGGING_ROOT = BASE_DIR / 'log'
LOGGING_ROOT.mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': f'{LOGGING_ROOT / "all.log"}',
            'backupCount': 24 * 7,
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cadocr_server': {
            'handlers': ['console', 'file', ] if enable_log_file else ['console', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


USE_I18N = False
USE_L10N = False
LANGUAGE_CODE = 'en-us'

USE_TZ = False
TIME_ZONE = 'Asia/Tokyo'

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = ()
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'