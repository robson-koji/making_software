

# Local configurations

# What is it for?
AMBIENTE = ''

# This is the Making Software home folder
# The folder where you unpack Making Software from Github
# if /home/your_name
INTELIFORM_PERL_DIR = ''

# You don´t have to change here, unless you have changed the create_projet.pl location
PERL_CREATE_PROJECT = INTELIFORM_PERL_DIR + '/making_software/making_software_perl/create_project.pl'

# This is the domain/subdmain to deploy created systems
# Change to suit your needs
SUBDOMINIO_PROJETOS = '192.168.1.100:8001'


# Django settings for Making Software project.
# It is considered that you are using a web server and WSGI to connect to
# Making Software Django application
# This urls are based on your virtual host configuration

VIRTUAL_HOST = '/making_software'
SESSION_COOKIE_PATH = '/making_software'

ADMIN_MEDIA_PREFIX = VIRTUAL_HOST + '/admin/'
LOGIN_REDIRECT_URL = VIRTUAL_HOST + '/flat/instrucoes/'

LOGIN_URL = VIRTUAL_HOST + '/accounts/login/'
LOGOUT_URL = VIRTUAL_HOST + '/accounts/logout/'


# Folder where your projects are created.
MEDIA_ROOT = '/home/making_software/projetos/'
MEDIA_URL = '/logos/'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# allauth options.
# Check allauth if you need help
ACCOUNT_AUTHENTICATION_METHOD = ("username")
ACCOUNT_EMAIL_VERIFICATION = ("mandatory")
SOCIALACCOUNT_EMAIL_VERIFICATION = ("none")
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True


EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
#EMAIL_HOST_USER
#EMAIL_HOST_PASSWORD


# Number of days to activate account sent by mail.
#ACCOUNT_ACTIVATION_DAYS = 7


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',             # Or path to database file if using sqlite3.
        'USER': '',             # Not used with sqlite3.
        'PASSWORD': '',                 # Not used with sqlite3.

        # isso eh muito importante, eh onde estah o socket do postgres instalado por default
        # O psycopg2 expects Postgres socket to be in /var/run/postgresql/
        #http://stackoverflow.com/questions/5500332/cant-connect-the-postgresql-with-psycopg2
        'HOST': '/tmp/',                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                     # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['']

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/var/www/static_files/making_software'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static_files/making_software/'


# Additional locations of static files
STATICFILES_DIRS = (
    "",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
# See this: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# You can generate a new one here:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '0$pp6prmm&^iulhtammo^hrzrdj(8@i@t3_ioasjeyj&65^+_n'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

)

ROOT_URLCONF = 'loopware.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'loopware.wsgi.application'


# If you move templates for another location, change here to
# the new address
TEMPLATE_DIRS = (
    INTELIFORM_PERL_DIR + '/making_software/loopware/templates/'
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.flatpages',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',

    'django.contrib.admin',
    'django.contrib.admindocs',
    
    'wysiwyg_forms',
    
    'bsct',
    
    'sistema',
    'elemento',
    'relacionamentos',
)


LOGGING = {
    'version': 1,
    #'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/mylog.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'request_handler': {
                'level':'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/django_request.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount'
)

