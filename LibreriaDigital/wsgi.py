"""
WSGI config for LibreriaDigital project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibreriaDigital.settings')
application = get_wsgi_application()
