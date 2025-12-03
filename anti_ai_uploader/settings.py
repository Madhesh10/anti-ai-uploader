# anti_ai_uploader/settings.py
import os
from pathlib import Path

# Optional: dj_database_url if you want DATABASE_URL support
try:
    import dj_database_url  # type: ignore
except Exception:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- SECURITY ----------
# secret from env (set on Render). Fallback is only for local dev.
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-unsafe-key-change-this")

# DEBUG must be "True" or "False" (string) in env; default False for safety
DEBUG = os.environ.get("DEBUG", "False") == "True"

# ALLOWED_HOSTS: comma-separated env var (set on Render to include your onrender domain)
raw_hosts = os.environ.get(
    "ALLOWED_HOSTS", ".onrender.com,anti-ai-uploader.onrender.com,localhost,127.0.0.1"
)
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

# CSRF trusted origins (comma separated)
_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "https://anti-ai-uploader.onrender.com")
CSRF_TRUSTED_ORIGINS = [u.strip() for u in _csrf_origins.split(",") if u.strip()]

# If deployed behind a HTTPS-terminating proxy (Render), set this:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Secure cookie settings (only applied when DEBUG is False)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

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
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # simple local sqlite fallback
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    }

# ---------- I18N / TIME ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")
USE_I18N = True
USE_TZ = True

# ---------- STATIC / MEDIA ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise storage (works with `collectstatic`)
STATICFILES_STORAGE = os.environ.get(
    "STATICFILES_STORAGE", "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

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

# ---------- SIMPLE LOGGING ----------
LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[%(levelname)s] %(asctime)s %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# ---------- Helpful debug note ----------
# If you are debugging on Render's free tier and cannot use the shell:
# - set DEBUG=True in Render env vars temporarily to view the Django debug page,
#   then set DEBUG=False after you capture the traceback and fixed the issue.
#
# For initial deploy troubleshooting, you may want DISABLE_COLLECTSTATIC=1 in Render env vars
# to avoid static collect issues while you get the app running. Then remove that var and run
# collectstatic once deploys succeed.
