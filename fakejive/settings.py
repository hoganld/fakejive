"""
Django settings for fakejive project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import saml2
import saml2.saml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4%%2kas6y#=i8h%6j(fo4_h5bde*+8!s8(t)2#7h5z-_wk42ny'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',
    'djangosaml2',
    'index',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)

ROOT_URLCONF = 'fakejive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fakejive.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# SAML STUFF
LOGIN_URL = '/saml/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_REDIRECT
SAML_CREATE_UNKNOWN_USER = False
SAML_DIR = os.path.join(BASE_DIR, 'saml')
IDP_URL = 'https://www.exdev.test/saml/saml2/idp/'

SAML_CONFIG = {
    # CHANGE THIS FOR YOUR SYSTEM
    'xmlsec_binary': '/usr/local/bin/xmlsec1',
    'entityid': 'https://localhost:8000/saml/metadata/',
    'attribute_map_dir': os.path.join(SAML_DIR, 'attributemaps'),
    'service': {
        'sp' : {
            'name': 'Fake Jive',
            'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
            'endpoints': {
                'assertion_consumer_service': [
                    ('https://localhost:8000/saml/acs/',
                     saml2.BINDING_HTTP_POST),
                ],
                'single_logout_service': [
                    ('https://localhost:8000/saml/ls/',
                     saml2.BINDING_HTTP_REDIRECT),
                    ('https://localhost:8000/saml/ls/post/',
                     saml2.BINDING_HTTP_POST),
                ],
            },
            'idp': {
                IDP_URL + 'metadata.php': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: IDP_URL + 'SSOService.php',
                    },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: IDP_URL + 'SingleLogoutService.php',
                    },
                },
            },
        },
    },
    'metadata': {
        'local': [os.path.join(SAML_DIR, 'idp_metadata.xml')],
    },
    'debug': 1,
    'key_file': os.path.join(SAML_DIR, 'fakejive.key'),  # private part
    'cert_file': os.path.join(SAML_DIR, 'fakejive.crt'),  # public part
    'encryption_keypairs': [{
        'key_file': os.path.join(SAML_DIR, 'fakejive.key'),  # private part
        'cert_file': os.path.join(SAML_DIR, 'fakejive.crt'),  # public part
    }],
    'contact_person': [
        {'given_name': 'Harry',
         'sur_name': 'Bovik',
         'company': 'Carnegie Mellon University',
         'email_address': 'bovik+@cs.cmu.edu',
         'contact_type': 'technical'},
    ],
}
