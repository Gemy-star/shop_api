from .base import *

# allow all hosts during development
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += ["silk"]

MIDDLEWARE += ['silk.middleware.SilkyMiddleware', ]
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

DEBUG = True
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
