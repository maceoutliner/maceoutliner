"""
Base settings for maceoutliner project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
import environ

if 'DATABASE_URL' not in os.environ.keys() and 'DATA_DB_USER' in os.environ.keys():
    if os.environ['DATA_DB_USER'] == 'nanobox':
        os.environ['DATABASE_URL'] = "postgres://{0}:{1}@{2}/gonano".format(os.environ['DATA_DB_USER'],
                                                                            os.environ['DATA_DB_PASS'],
                                                                            os.environ['DATA_DB_HOST'])
ROOT_DIR = environ.Path(__file__) - 3  # (maceoutliner/config/settings/base.py - 3 = maceoutliner/)
APPS_DIR = ROOT_DIR.path('maceoutliner')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'foundation_formtags',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'taggit',
    'treebeard',
    'rules.apps.AutodiscoverRulesConfig',
    'rest_framework',
    'rest_framework_rules',
    'django_q',
    'avatar',
    'registration',
    'pwned_passwords_django',
]

MACEOUTLINER_APPS = [
        'fiction_outlines',
        'fiction_outlines_api',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    'maceoutliner.users.apps.UsersConfig',
    # Your stuff: custom apps go here

]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + MACEOUTLINER_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'pwned_passwords_django.validators.PwnedPasswordsValidator',  Disabled because it makes runserver choke
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'maceoutliner.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Daniel Andrlik""", 'daniel@andrlik.org'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///maceoutliner'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 600


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'pwned_passwords_django.validators.PwnedPasswordsValidator',
    },
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_USERNAME_VALIDATORS = 'maceoutliner.users.validators.custom_validators'
ACCOUNT_ADAPTER = 'maceoutliner.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'maceoutliner.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# CELERY
# INSTALLED_APPS += ['maceoutliner.taskapp.celery.CeleryConfig']
# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
# if CELERY_BROKER_URL == 'django://':
#    CELERY_RESULT_BACKEND = 'redis://'
# else:
#    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# ######### END CELERY


# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["compressor", ]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder", ]

# django-libsass
COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'django_libsass.SassCompiler'),
]

COMPRESS_CACHEABLE_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = 'admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

# Avatar settings
# ------------------------------------------------------------------------------
AVATAR_EXPOSE_USERNAMES = False
AVATAR_GRAVATAR_DEFAULT = 'identicon'
AVATAR_CLEANUP_DELETED = True
AVATAR_AUTO_GENERATE_SIZES = (80, 30)
AVATAR_GRAVATAR_BASE_URL = 'https://www.gravatar.com/avatar/'
