"""
WSGI config for cozysiren project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import logging
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.append(BASE_DIR)

#if not settings.DEBUG:
try:
    if os.environ['RACK_ENV'] == 'production':
        import newrelic.agent
        newrelic.agent.initialize('/usr/local/etc/newrelic.ini')
except:
    logging.error("No RACK_ENV or New Relic file")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#application = newrelic.agent.wsgi_application()(application)