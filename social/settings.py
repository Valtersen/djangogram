import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-vufjclp8qq2gl#hjs2u+qx0*u31^egite8u8cl^)13*%qpd7j('

DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = ['djangogram-v.herokuapp.com', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'djangogram',
    'taggit',
    'allauth',
    'allauth.account',
    'whitenoise.runserver_nostatic',
    'allauth.socialaccount',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  #WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'social.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2vcb6s89uvnrc',
        'USER': 'huaswolmztxwix',
        'PASSWORD': 'cde4b518f89e6d5a5657c757abc00a7a4b5370810c001f7986ffc254c05e35b0',
        'HOST': 'ec2-54-75-184-144.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'djangogram.DUser'


LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

ACCOUNT_EMAIL_VERIFICATION = "optional"  # "mandatory"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_SIGNUP_FORM_CLASS = 'djangogram.forms.DUserCreationForm'

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'home'

ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'home'

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True


EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', '')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', '')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'hi1pjd7bl',
    'API_KEY': '511966933532915',
    'API_SECRET': 'N7nk081qV6JxV6daKv4JWzJNTL0',
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DEFAULT_FILE_STORAGE, 'media')  # os.path.join(STATIC_ROOT, 'media')