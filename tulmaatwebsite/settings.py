"""
Django settings for tulmaatwebsite project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load a local .env file if present (safe no-op on Render, where you set
# env vars directly in the dashboard instead of via a file).
try:
    from dotenv import load_dotenv 
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Core security settings — all driven by environment variables.
# NEVER commit real secret values; set these in Render's dashboard
# (Environment tab) for production and in a local, git-ignored .env file
# for development. See .env.example for the full list.
# ---------------------------------------------------------------------------

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    # Fallback ONLY for first-time local setup — replace it by setting
    # DJANGO_SECRET_KEY, then delete this fallback. Never deploy with it.
    'django-insecure-CHANGE-ME-generate-a-new-key',
)

# Defaults to False (safe) — set DJANGO_DEBUG=True only on your own machine.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get(
        'DJANGO_ALLOWED_HOSTS', 'tulmaatwebsiteg.onrender.com'
    ).split(',')
    if h.strip()
]
if DEBUG:
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tulmaatwebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tulmaatwebsite.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# To move to Postgres on Render, set DATABASE_URL and swap in dj_database_url:
# import dj_database_url
# DATABASES['default'] = dj_database_url.config(default=os.environ['DATABASE_URL'])

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# STATICFILES_DIRS points at the folder your images/css/js actually live in
# (project-level `static/`). STATIC_ROOT is a separate folder that
# `collectstatic` builds for Whitenoise to serve in production — it should
# never be the same folder as your source static files.
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "staticfiles": {
        # CompressedStaticFilesStorage still gzips/brotli-compresses files for
        # fast delivery, but — unlike CompressedManifestStaticFilesStorage —
        # it does NOT require every {% static %} reference (including Django
        # admin's own CSS/JS) to exist in a prebuilt manifest before the page
        # can render. A missing file just 404s instead of crashing the page.
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Email — used for booking confirmation messages.
# In development (no EMAIL_HOST_USER set), emails print to the console
# instead of actually sending, so you can test bookings without SMTP
# credentials. In production, set the EMAIL_* env vars (see .env.example).
# ---------------------------------------------------------------------------
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')

if EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'Tulmaat Hotel <no-reply@tulmaathotel.com>'
)

# ---------------------------------------------------------------------------
# Extra hardening — only meaningful once DEBUG=False behind HTTPS (Render
# terminates TLS for you, so these are safe to enable there).
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_CONTENT_TYPE_NOSNIFF = True