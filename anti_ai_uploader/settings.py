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
# SECRET_KEY: read from env, fallback to a local dev key
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-unsafe-key-change-this")

# DEBUG: read from env as string and convert to boolean
# Use "True" (capital T) to enable debug on purpose. Default is False for safety.
DEBUG = os.environ.get("DEBUG", "False") == "True"

# read ALLOWED_HOSTS from env var (comma separated), fallback to sensible defaults
_raw_hosts = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,.onrender.com")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

# CSRF trusted origins — also allow setting via env var (comma separated)
_csrf_origins = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "https://anti-ai-uploader.onrender.com"
)
CSRF_TRUSTED_ORIGINS = [u.strip() for u in _csrf_origins.split(",") if u.strip()]

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
    # WhiteNoise is present to serve static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------- STATIC / MEDIA ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise compressed manifest storage (works with `collectstatic`)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------- FILE STORAGE (optional S3) ----------
USE_S3 = os.getenv("USE_S3", "False").lower() == "true"
if USE_S3:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# ---------- DEFAULT AUTO FIELD ----------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
