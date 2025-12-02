# anti_ai_uploader/settings.py
import os
from pathlib import Path

# try import dj_database_url safely
try:
    import dj_database_url
except Exception:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- SECURITY ----------
# Robust SECRET_KEY handling: if env var is missing OR empty,
# use a local dev fallback.
_env_secret = os.getenv("SECRET_KEY", "").strip()

if _env_secret:
    SECRET_KEY = _env_secret
else:
    # only for local development – change in real production if you want
    SECRET_KEY = "dev-unsafe-key-change-this"

# DEBUG: False in production, True on your laptop
DEBUG = os.getenv("DEBUG", "True") == "True"

# Allow local dev + any Render app domain
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",  # anti-ai-uploader.onrender.com
]

# Trust your Render origin for CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://anti-ai-uploader.onrender.com",
]

# ---------- INSTALLED APPS ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "uploader",
]

# ---------- MIDDLEWARE ----------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static files in production
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

# ---------- TEMPLATES ----------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------- I18N / TIME ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"   # India time
USE_I18N = True
USE_TZ = True

# ---------- STATIC / MEDIA ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Optional S3 config (off by default)
USE_S3 = os.getenv("USE_S3", "False") == "True"
if USE_S3:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# ---------- DEFAULT AUTO FIELD ----------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
