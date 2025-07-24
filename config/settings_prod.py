from .settings_base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'erp.midominio.com').split(',')
