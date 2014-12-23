"""
Django settings for cozysiren project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

#from logging.handlers import SysLogHandler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

POSTGIS_VERSION = (2, 1, 1)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if "DJANGO_SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    SECRET_KEY = 'ABCDEFG'

if "GCM_API_KEY" in os.environ:
    GCM_API_KEY = os.environ['GCM_API_KEY']
else:
    GCM_API_KEY = None

if "MANDRILL_API_KEY" in os.environ:
    MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    DEFAULT_FROM_EMAIL = 'no-reply@alerted.us'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

ON_DOCKER = False
ON_DOCKER_PROD = False
ON_FIG = False
ON_DO = False
ON_SNAP_CI = False

# Enable this to view the toolbar
ENABLE_DEBUG_TOOLBAR = False

DEBUG = False
if 'RACK_ENV' in os.environ:
    if os.environ['RACK_ENV'] == "development":
        DEBUG = True
        ON_DOCKER = True
    elif os.environ['RACK_ENV'] == "production":
        ON_DO = True
    elif os.environ['RACK_ENV'] == "testing":
        ON_SNAP_CI = True
    elif os.environ['RACK_ENV'] == "production_docker":
        ON_DOCKER_PROD = True
        DEBUG = True

if ON_DO:
    REDIS_PASSWORD = ""
    REDIS_ENDPOINT = os.environ["REDIS_ENDPOINT"]
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_URL = '%s:%s:1' % (REDIS_ENDPOINT, REDIS_PORT)
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASSWD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']

elif ON_SNAP_CI:
    REDIS_PASSWORD = ""
    REDIS_ENDPOINT = os.environ["REDIS_ENDPOINT"]
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_URL = '%s:%s:1' % (REDIS_ENDPOINT, REDIS_PORT)
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['SNAP_DB_PG_USER']
    DB_PASSWD = os.environ['SNAP_DB_PG_PASSWORD']
    DB_HOST = os.environ['SNAP_DB_PG_HOST']
    DB_PORT = os.environ['SNAP_DB_PG_PORT']

elif ON_DOCKER_PROD:
    REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
    REDIS_ENDPOINT = os.environ["REDIS_PORT_6379_TCP_ADDR"]
    REDIS_PORT = os.environ["REDIS_PORT_6379_TCP_PORT"]
    REDIS_URL = '%s:%s:1' % (REDIS_ENDPOINT, REDIS_PORT)
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASSWD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']

elif ON_DOCKER:  # Default catch all
    REDIS_PASSWORD = ""
    REDIS_ENDPOINT = "redis"
    REDIS_PORT = 6379
    REDIS_URL = '%s:%d:1' % (REDIS_ENDPOINT, REDIS_PORT)
    DB_NAME = 'cozysiren'
    DB_USER = 'app_user'
    DB_PASSWD = 'djangouserspassword'
    DB_HOST = 'db'
    DB_PORT = '5432'

else:
    REDIS_PASSWORD = ""
    REDIS_ENDPOINT = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_URL = '%s:%d:1' % (REDIS_ENDPOINT, REDIS_PORT)
    DB_NAME = 'cozysiren'
    DB_USER = 'app_user'
    DB_PASSWD = 'djangouserspassword'
    DB_HOST = '127.0.0.1'
    DB_PORT = '5432'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [".alerted.us", ".tutum.io", "trusty64", "172.17.8.101", ".amazonaws.com", "localhost"]

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
    'djrill',
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'django_nose',
    "push_notifications",
)

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar.apps.DebugToolbarConfig',
    )
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

PUSH_NOTIFICATIONS_SETTINGS = {
    "GCM_API_KEY": GCM_API_KEY,
}

# When using TCP connections
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'PASSWORD': REDIS_PASSWORD,  # Optional
            'CONNECTION_POOL_KWARGS': {'max_connections': 1000}
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

MIDDLEWARE_CLASSES = (
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

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


INTERNAL_IPS = ('127.0.0.1', '10.0.2.2', '10.69.18.71')

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
        'rest_framework.renderers.XMLRenderer',
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
    "allauth.account.context_processors.account",

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

LOGIN_REDIRECT_URL = '/dashboard/locations/'

ACCOUNT_LOGOUT_ON_GET = True

# Stuff for celery

BROKER_URL = 'redis://%s:%s/0' % (REDIS_ENDPOINT, REDIS_PORT)
CELERY_RESULT_BACKEND = BROKER_URL

BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

if DEBUG:
    CELERY_ALWAYS_EAGER = True

ADMINS = (('Kelvin', 'kelvin@kelvinism.com'), )

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
