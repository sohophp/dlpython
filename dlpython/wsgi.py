"""
WSGI config for dlpython project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(1,'/usr/local/lib/python3.8/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dlpython.settings')

application = get_wsgi_application()
