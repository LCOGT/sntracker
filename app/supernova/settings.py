import os, sys
from django.utils.crypto import get_random_string

VERSION = '0.1'

TEST = 'test' in sys.argv
COMPRESS_ENABLED = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

PRODUCTION = True if CURRENT_PATH.startswith('/var/www') else False
DEBUG = False

HOME = os.environ.get('HOME','/tmp')

MANAGERS = ADMINS
SITE_ID = 1

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        'NAME': os.environ.get('SNTRACKER_DB_NAME', ''),
        "USER": os.environ.get('SNTRACKER_DB_USER', ''),
        "PASSWORD": os.environ.get('SNTRACKER_DB_PASSWD', ''),
        "HOST": os.environ.get('SNTRACKER_DB_HOST', ''),
        "OPTIONS": {'init_command': 'SET default_storage_engine=INNODB'} if PRODUCTION else {},
        "PORT" : 3306,
        }
    }

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'observe.apps.ObserveConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'supernova.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'supernova.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_ROOT = '/var/www/html/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'observe'),]

MEDIA_URL = "/media/"
MEDIA_ROOT = '/var/www/apps/sntracker/observe/media/'

FFMPEG = '/bin/ffmpeg'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS       = True
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_HOST_USER     = os.environ.get('SNTRACKER_EMAIL_USERNAME','')
EMAIL_HOST_PASSWORD = os.environ.get('SNTRACKER_EMAIL_PASSWORD','')
EMAIL_PORT          =  587
DEFAULT_FROM_EMAIL  = 'Supernova Tracker <streams-admin@lco.global>'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'supernova.log',
            'formatter': 'verbose',
            'filters': ['require_debug_false']
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
            'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'supernova': {
            'handlers':['console'],
            'level' : 'DEBUG'
        }
    }
}

API_URL = 'https://lco.global/observe/api/user_requests/'
ARCHIVE_TOKEN_API = 'https://archive-api.lco.global/api-token-auth/'
OBSERVE_TOKEN_API = 'https://lco.global/observe/api/api-token-auth/'

PROPOSAL_USER = os.environ.get('PROPOSAL_USER','')
PROPOSAL_PASSWD = os.environ.get('PROPOSAL_PASSWD','')
PROPOSAL_CODE = os.environ.get('PROPOSAL_CODE','')

if not CURRENT_PATH.startswith('/var/www'):
    try:
        from local_settings import *
    except ImportError as e:
        if "local_settings" not in str(e):
            raise e
