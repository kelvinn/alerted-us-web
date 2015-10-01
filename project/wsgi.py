"""
WSGI config for cozysiren project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import logging
from dj_static import Cling

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.append(BASE_DIR)

try:
    if os.environ['RACK_ENV'] in ['staging', 'production']:
        import newrelic.agent
        newrelic.agent.initialize()
except:
    logging.error("Error starting NewRelic agent")

from django.core.wsgi import get_wsgi_application
application = Cling(get_wsgi_application())
