import os
from django.conf import settings



SECRET_KEY = '^aaz(sb^g_n%)!x46z9e)o&ovq*ky035m1(%$nr)5=g+jo#tx3'

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = settings.DATABASES

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_ACCESS_KEY_ID = 'AKIAIXCOMXT3BTDJK3EA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'sockcessfullydone'
STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'