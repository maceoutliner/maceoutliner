"""
Local settings for maceoutliner project.

- Run in Debug mode

- Use mailhog for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)  # noqa: F405
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default=')i$cc:^%C=AKrX~<36!ywm&^sn-v$F8Q~6m5r)4ReyTR!<r[&*')  # noqa: F405

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'


# CACHING
# ------------------------------------------------------------------------------
REDIS_URL = env('REDIS_URL', default=None)  # noqa: F405
if not REDIS_URL:
    # try to construct it from other variables
    REDIS_HOST = env('REDIS_HOST', default=None)  # noqa: F405
    if REDIS_HOST:
        REDIS_URL = "redis://{}:6379".format(REDIS_HOST)
if REDIS_URL:
    CLIENT_CLASS = env('CLIENT_CLASS', default=None)  # noqa: F405
if REDIS_URL and CLIENT_CLASS:
    REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL', default=''), 0)  # noqa: F405
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_LOCATION,  # noqa: F405,
            'OPTIONS': {
                "CLIENT_CLASS": CLIENT_CLASS,
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND':  env('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),  # noqa: F405
            'LOCATION': '',
        }
    }

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]  # noqa: F405
INSTALLED_APPS += ['debug_toolbar', ]  # noqa: F405

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
ALLOWED_HOSTS = ['django.local']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# ######### CELERY
# In development, all tasks will be executed locally by blocking until the task returns
# CELERY_ALWAYS_EAGER = True
# ######### END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
if REDIS_URL:
    Q_CLUSTER = {
        'name': 'DJRedis',
        'workers': 4,
        'timeout': 90,
        'django_redis': 'default',
    }
else:
    Q_CLUSTER = {
        'name': 'DjangORM',
        'workers': 4,
        'timeout': 90,
        'retry': 120,
        'queue_limit': 50,
        'bulk': 10,
        'orm': 'default',
        'sync': True,
    }
