# anti_ai_uploader/settings.py
import os
from pathlib import Path

# try import dj_database_url safely
try:
    import dj_database_url
except Exception:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")

# === LOCAL DEBUG SETTINGS (DEV ONLY) ===
# Turn on debug locally to see full tracebacks. Make sure to set DEBUG=False in production.
DEBUG = True

# Allow local hosts for development
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

# ---------- INSTALLED APPS ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",   # required for collectstatic & static handling
    "uploader",                      # your app (ensure this exists)
]

# ---------- MIDDLEWARE ----------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------- URL / WSGI ----------
ROOT_URLCONF = "anti_ai_uploader.urls"
WSGI_APPLICATION = "anti_ai_uploader.wsgi.application"

# ---------- TEMPLATES (minimal) ----------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ensure this folder exists for your site-level templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------- DATABASES ----------
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL and dj_database_url:
    # If you set a DATABASE_URL env var and dj_database_url is available, use it
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # Local SQLite default (works for dev and avoids missing ENGINE errors)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------- AUTH / I18N ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------- STATIC / MEDIA ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS should point to your project-level static folder (if used)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Use whitenoise in production for static file serving (keeps STATICFILES_STORAGE unless USE_S3)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Only enable S3 if explicitly asked via env
USE_S3 = os.getenv("USE_S3", "False") == "True"
if USE_S3:
    # If you enable S3, make sure environment AWS vars are set and 'django-storages' is installed.
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# ---------- DEFAULT AUTO FIELD ----------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
