"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from datetime import timedelta

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True  # turning false to allow error 500 displayed as json
DEBUG = int(os.environ.get("DEBUG", default=0))

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

APPEND_SLASH = False  # REMOVE THE TRAILING SLASH IN URL e.g http://127.0.0.1:8000/

ADMINS = [('Benson', 'bensonowinoopondo@gmail.com'), ('Owino', 'owinoben2020@ggmail.com')]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # documentation
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Monitoring
    'django_prometheus',

    'base',
    'auth_apps',
    'products',
    'checkout',
    'googleMaps',
    'orders',
    'categories',
    'socialAuth',
    'address',
    'dashboard',
    'report',
    'merchant',
    'setting',
    'payments'

]

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 24,

    # 'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'EXCEPTION_HANDLER': 'utils.errors.exceptionhandler.customExceptionHandler',

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata'

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Ecommerce Api Documentation',
    'DESCRIPTION': 'Welcome to the Ecommerce API reference! It contains a guide on how to integrate to our API and '
                   'outlines important information to assist you through the integration process. The API is a REST '
                   'API over HTTP using JSON as the exchange format. It uses standard HTTP response codes, '
                   'authentication, and verbs.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # OTHER SETTINGS
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

AUTH_USER_MODEL = 'auth_apps.Account'

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'middleware.middleware.CustomHeaderMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_prometheus.middleware.PrometheusAfterMiddleware',

]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER", "user"),
        'HOST': os.environ.get("DB_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", "5432"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "password"),

        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'patazonedb',
        # 'USER': 'admin',
        # 'HOST': 'ec2-34-198-48-156.compute-1.amazonaws.com',
        # 'PORT': '3306',
        # 'PASSWORD': 'patazone123',

        # 'NAME': 'admin_patazone',
        # 'USER': 'root',
        # 'HOST': '127.0.0.1',
        # 'PORT': '3306',
        # 'PASSWORD': 'patazone123',
    }

}

CACHES = {
    'default': {
        'BACKEND': 'django_prometheus.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'ecommerce-backend:11211',
    }
}

if 'test' in sys.argv or 'test\_coverage' in sys.argv:  # Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES['default']['NAME'] = ':memory:'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://localhost:1337']
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ['http://localhost:1337']
