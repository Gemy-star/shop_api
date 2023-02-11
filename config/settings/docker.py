from .base import *


ALLOWED_HOSTS = []
DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'brandDB',
        'USER': 'root',
        'PASSWORD': 'gemy2803150',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8'  # This is the relevant line
        }
    }
}
