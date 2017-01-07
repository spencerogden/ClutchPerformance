from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'outbound.mailhop.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'spencerogden'
EMAIL_HOST_PASSWORD = 'vrpt@7GPcwej'
EMAIL_USE_SSL = True

ALLOWED_HOSTS = ['spencerogden.pythonanywhere.com']

STATIC_ROOT = os.path.join(PROJECT_HOME, "static")