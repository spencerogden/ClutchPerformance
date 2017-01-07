from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'outbound.mailhop.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'spencerogden'
EMAIL_HOST_PASSWORD = 'vrpt@7GPcwej'
EMAIL_USE_SSL = True
