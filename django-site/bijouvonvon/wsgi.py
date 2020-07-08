"""
WSGI config for bijouvonvon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

if "" not in sys.path:
    sys.path = [""] + sys.path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bijouvonvon.settings')

application = get_wsgi_application()
