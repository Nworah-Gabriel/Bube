import os
import cloudinary
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRETKEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

ADDED_PACKAGES = [
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "cloudinary_storage",
    "cloudinary",
]

DJANGO_APPS = [
    "Admin",
    "Website"
]

INSTALLED_APPS = DEFAULT_APPS + ADDED_PACKAGES + DJANGO_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


USER_AGENTS_CACHE = 'default'

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            ],
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

WSGI_APPLICATION = 'core.wsgi.application'
AUTH_USER_MODEL = "Admin.User"
DEVELOPMENT_MODE = True


if not DEVELOPMENT_MODE:
    BACKEND_URL = 'https://house4rent-qa8s.onrender.com'
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
else:
    BACKEND_URL = 'http://localhost:8000'
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Africa/Algiers"
USE_I18N = True
USE_TZ = True

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("_CLOUD_NAME"),
    "API_KEY": os.getenv("_API_KEY"),
    "API_SECRET": os.getenv("_API_SECRET"),
}
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"],
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILE_DIR = [
    os.path.join(BASE_DIR, "Admin/static"),
    os.path.join(BASE_DIR, "Website/static")
    ]
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%b %d, %Y - %I:%M %p",
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.tokens.BearerAuthentication",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
}

#   Corsheaders - Restrict ports address connecting to API's
CORS_ALLOWED_ORIGINS_REGEXES = [
    r"^http://localhost:\d+$",   
    r"^http://127\.0\.0\.1:\d+$",
]

CORS_ALLOWED_ORIGINS = [ 
    "https://house4rent-qa8s.onrender.com",
    "https://house4rent-admin.vercel.app",
]


CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS + CORS_ALLOWED_ORIGINS_REGEXES
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",
    "accept",
    "accept-encoding",
    "accept-language",
]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
