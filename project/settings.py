"""
Django settings for cozysiren project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

POSTGIS_VERSION = (2, 1, 1)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'ABCDEFG')

if "GCM_API_KEY" in os.environ:
    GCM_API_KEY = os.environ['GCM_API_KEY']
else:
    GCM_API_KEY = None

if "MAILGUN_API_KEY" in os.environ:

    MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']

    ANYMAIL = {
        # (exact settings here depend on your ESP...)
        "MAILGUN_API_KEY": MAILGUN_API_KEY,
        "MAILGUN_SENDER_DOMAIN": 'mg.alerted.us',  # your Mailgun domain, if needed
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    DEFAULT_FROM_EMAIL = 'no-reply@alerted.us'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# Enable this to view the toolbar
ENABLE_DEBUG_TOOLBAR = False
    
DEBUG = False

# This will force debug to be on if using the development server or if set in an env variable
if not len(sys.argv) < 2:
    if sys.argv[1] == 'runserver':
        ENABLE_DEBUG_TOOLBAR = True
        DEBUG = True
elif os.getenv('DEBUG', 'False') == 'True':
    ENABLE_DEBUG_TOOLBAR = True
    DEBUG = True

OPBEAT = {
    'ORGANIZATION_ID': os.getenv("ORGANIZATION_ID", ''),
    'APP_ID': os.getenv("APP_ID", ''),
    'SECRET_TOKEN': os.getenv("SECRET_TOKEN", ''),
}

LOGZ_TOKEN = os.getenv("LOGZ_TOKEN", '')
LOGZ_URL = os.getenv("LOGZ_URL", '')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [".alerted.us", "127.0.0.1", "192.168.83.*", ".tutum.io", ".kelvinism.com", "trusty64", "172.17.8.101",
                 ".herokuapp.com", "127.*.*.*", "localhost", ".rhcloud.com"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'apps.alertdb',
    'apps.people',
    'django.contrib.admin',
    'bootstrapform',
    'anymail',
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'opbeat.contrib.django',
)


# Show toolbar to anybody when enabled
def show_toolbar(request):
    return True


if DEBUG and ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
    )


    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK' : show_toolbar,
    }

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.alertdb.middleware.ProfilerMiddleware',
)

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

TEST_OUTPUT_DIR = 'reports'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=apps.people',
    '--cover-package=apps.alertdb',
    '--with-xunit',
    '--xunit-file=reports/nosetests.xml'
]

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates/"),
    os.path.join(BASE_DIR, "templates/admin/"),
    os.path.join(BASE_DIR, "templates/admin/alertdb/alert/"),
    os.path.join(BASE_DIR, "templates/admin/alertdb/info/"),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}

DATABASES['default'] = dj_database_url.config(default='postgis://postgres:password@127.0.0.1:5432/postgres', conn_max_age=600)


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

INTERNAL_IPS_ENV = os.getenv('INTERNAL_IP', '')
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2', '10.69.18.71', '123.243.19.133', INTERNAL_IPS_ENV)

STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125
STATSD_PREFIX = None
STATSD_MAXUDPSIZE = 512

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR + '/static'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps/static/'),
)

REST_FRAMEWORK = {
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'apps.alertdb.api.CAPXMLParser'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    """
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    """
    'PAGINATE_BY': 10
}


TEMPLATE_CONTEXT_PROCESSORS = (

    # Required by allauth template tags
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    # allauth specific context processors
    #"allauth.account.context_processors.account",

)

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

LOGIN_REDIRECT_URL = '/dashboard/settings/'

ACCOUNT_LOGOUT_ON_GET = True



BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

if DEBUG:
    CELERY_ALWAYS_EAGER = True

ADMINS = (('Admin', 'admin@alerted.us'), )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'logzioFormat': {
            'format': '{"additional_field": "value"}'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose'
        },
        'logzio': {
            'class': 'logzio.handler.LogzioHandler',
            'level': 'INFO',
            'formatter': 'logzioFormat',
            'token': LOGZ_TOKEN,
            'logzio_type': "django",
            'logs_drain_timeout': 5,
            'url': LOGZ_URL,
            'debug': True
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'appname': {
            'handlers': ['console', 'logzio'],
            'level': 'INFO'
        }
    }
}