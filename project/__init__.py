from __future__ import absolute_import
import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
if 'RACK_ENV' in os.environ:
    if os.environ['RACK_ENV'] != 'openshift':
        from .celery import app as celery_app
