# -*- coding: utf-8 -*-
import os, sys

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(CURRENT_PATH)

SECRET_KEY = '8drogeie6q2a9zw(7%-n2x8hr!4(x+*^8=-23tl!$n!vk@!-w7'

PREFIX =""
DEBUG = True
PRODUCTION = False
STATIC_ROOT =  '/Users/egomez/Sites/static/'

MEDIA_ROOT = '/Users/egomez/code/django/supernova/app/observe/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'observe'),]
PROPOSAL_USER = 'streams-admin@lcogt.net'
PROPOSAL_PASSWD = 'darkskies0'
FFMPEG = 'ffmpeg'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",#sqlite3",
        "NAME": "supernova",#.db",
        "USER": "root",
        "PASSWORD":  "",
        "HOST": "127.0.0.1"
    }
}

DJANGO_LIVE_TEST_SERVER_ADDRESS="localhost:8000-8010,8080,9200-9300"

if 'test' in sys.argv:
    # Use SQLite3 for the database engine during testing.
    print("Using test sqlite DB")
    DATABASES = {'default':
            {'ENGINE': 'django.db.backends.sqlite3',
                                 'HOST': '',
                                 'NAME': CURRENT_PATH + 'test.sqlite',
                                 'OPTIONS': {},
                                 'PASSWORD': '',
                                 'PORT': '',
                                 'TEST_CHARSET': None,
                                 'TEST_COLLATION': None,
                                 'TEST_MIRROR': None,
                                 'TEST_NAME': None,
                                 'TIME_ZONE': 'UTC',
                                 'USER': 'root'
                    },
                }
