import ast
import sys
import os

TEST = 'test' in sys.argv
COMPRESS_ENABLED = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

MANAGERS = ADMINS
SITE_ID = 1

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': os.environ.get('DB_NAME', ''),
        "USER": os.environ.get('DB_USER', ''),
        "PASSWORD": os.environ.get('DB_PASS', ''),
        "HOST": os.environ.get('DB_HOST', ''),
        "PORT" : "5432",
        }
    }

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', None)
if not SECRET_KEY:
    print('ERROR: You must specify the Django secret key!')
    sys.exit(1)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))

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
    'pagedown',
    'markdown_deux',
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

PAGEDOWN_SHOW_PREVIEW = True

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
    },
}

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'observe','static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'

OBSERVE_URL = 'https://lco.global/observe/api/'
API_URL = 'https://lco.global/observe/api/user_requests/'
TOKEN_API = 'api-token-auth/'
THUMBNAIL_URL = 'https://thumbnails.lco.global/'
ARCHIVE_URL = 'https://archive-api.lco.global/'
SCHEDULE_API_URL = 'https://lco.global/observe/service/request/submit'
CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID','')
CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET','')

OBSERVE_TOKEN_URL = 'https://lco.global/observe/o/token/'
ARCHIVE_TOKEN_URL = "{}{}".format(ARCHIVE_URL, TOKEN_API)
ARCHIVE_TOKEN_API = os.path.join(ARCHIVE_URL, TOKEN_API)

ARCHIVE_TOKEN = os.environ.get('ARCHIVE_TOKEN','')
ODIN_TOKEN = os.environ.get('ODIN_TOKEN','')

PROPOSAL_USER = os.environ.get('PROPOSAL_USER','')
PROPOSAL_PASS = os.environ.get('PROPOSAL_PASS','')
PROPOSAL_CODE = os.environ.get('PROPOSAL_CODE','')
FFMPEG = '/bin/ffmpeg'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS       = True
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_HOST_USER     = os.environ.get('EMAIL_USER','')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS','')
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
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'supernova': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}
