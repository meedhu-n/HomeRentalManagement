"""
Clean minimal placeholder settings for HomeRentalManagement package.

This file replaces a corrupted settings.py that contained an unterminated
string. The real project settings live in the `config` package (see manage.py).
"""
from pathlib import Path

# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Development-only secret key (replace for production)
SECRET_KEY = 'django-insecure-replaced-secret-key-please-change'

DEBUG = True

ALLOWED_HOSTS = []

# Minimal installed apps to keep imports safe
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Media files (for uploaded property images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Razorpay Payment Configuration
RAZORPAY_KEY_ID = 'rzp_test_YOUR_KEY_ID'  # Replace with your Razorpay test/live key
RAZORPAY_KEY_SECRET = 'rzp_test_YOUR_KEY_SECRET'  # Replace with your Razorpay test/live secret
PROPERTY_REGISTRATION_FEE = 100  # Amount in INR (e.g., 100 INR = ~$1.20 USD)

# Database (minimal SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# trimmed by script
