"""
Django settings for routechoices project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import environ

from routechoices.slug_blacklist import SLUG_BLACKLIST

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Environment dependent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY")

PARENT_HOST = env.str("PARENT_HOST")
LOGIN_URL = env.str("LOGIN_URL")
REDIRECT_ALLOWED_DOMAINS = env.list("REDIRECT_ALLOWED_DOMAINS")
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN")
STATIC_URL = env.str("STATIC_URL")

CSP_DEFAULT_SRC = env.list("CSP_DEFAULT_SRC")
CSP_STYLE_SRC = env.list("CSP_STYLE_SRC")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

POST_LOCATION_SECRETS = env.list("POST_LOCATION_SECRETS")

BANNED_COUNTRIES = env.list("BANNED_COUNTRIES")

DATABASES = {"default": env.db()}
# DATABASES["default"]["CONN_MAX_AGE"] = env.int("DATABASE_CONN_MAX_AGE")
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True
try:
    DATABASES["default"]["OPTIONS"]["pool"] = True
    DATABASES["default"]["OPTIONS"]["server_side_binding"] = True
except Exception:
    pass

SHORTCUT_BASE_URL = env.str("SHORTCUT_BASE_URL", None)

AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")

EMAIL_CONFIG = env.email()
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
EMAIL_CUSTOMER_SERVICE = env.str("EMAIL_CUSTOMER_SERVICE")

ANALYTICS_API_KEY = env.str("ANALYTICS_API_KEY")
ANALYTICS_API_URL = env.str("ANALYTICS_API_URL")

LEMONSQUEEZY_SIGNATURE = env.str("LEMONSQUEEZY_SIGNATURE")
LEMONSQUEEZY_API_KEY = env.str("LEMONSQUEEZY_API_KEY")
LEMONSQUEEZY_STORE_ID = env.str("LEMONSQUEEZY_STORE_ID")
LEMONSQUEEZY_PRODUCTS_VARIANTS = env.list("LEMONSQUEEZY_PRODUCTS_VARIANTS")


RELYING_PARTY_ID = env.str("RELYING_PARTY_ID")
RELYING_PARTY_NAME = env.str("RELYING_PARTY_NAME")
ACCOUNT_EMAIL_VERIFICATION = env.str("ACCOUNT_EMAIL_VERIFICATION")

# Leave content below as it is
ALLOWED_HOSTS = ["*"]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
INSTALLED_APPS = [
    "routechoices",
    "routechoices.core",
    "routechoices.lib",
    "django_bootstrap5",
    "django_hosts",
    "corsheaders",
    "user_sessions",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "invitations",
    "background_task",
    "admincommand",
    "oauth2_provider",
    "rest_framework",
    "drf_yasg",
    "markdownify.apps.MarkdownifyConfig",
    "django_s3_storage",
    "qr_code",
    "kagi",
    "compressor",
    "hijack",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]
MIDDLEWARE = [
    "routechoices.core.middleware.SessionMiddleware",
    "routechoices.core.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "routechoices.core.middleware.XForwardedForMiddleware",
    "routechoices.core.middleware.FilterCountriesIPsMiddleware",
    "routechoices.core.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.common.CommonMiddleware",
    "routechoices.core.middleware.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_minify_html.middleware.MinifyHtmlMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "hijack.middleware.HijackUserMiddleware",
]
SESSION_ENGINE = "user_sessions.backends.db"
ROOT_URLCONF = "routechoices.urls"
ROOT_HOSTCONF = "routechoices.hosts"
DEFAULT_HOST = "www"
TEMPLATES_LOADERS = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ),
]
TEMPLATES_CONTEXT_PROCESSORS = [
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "routechoices.lib.context_processors.site",
]
if DEBUG:
    TEMPLATES_LOADERS = [
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    ]
    TEMPLATES_CONTEXT_PROCESSORS = [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "routechoices.lib.context_processors.site",
    ]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": TEMPLATES_LOADERS,
            "context_processors": TEMPLATES_CONTEXT_PROCESSORS,
        },
    },
]
WSGI_APPLICATION = "routechoices.wsgi.application"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
TIME_ZONE = "UTC"
USE_TZ = True
SITE_ID = 1
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_assets"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
LOGIN_REDIRECT_URL = f"//www.{PARENT_HOST}/dashboard"
LOGOUT_REDIRECT_URL = f"//www.{PARENT_HOST}"
SESSION_COOKIE_SAMESITE = None
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "drf_orjson_renderer.renderers.ORJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}
ACCOUNT_ADAPTER = "routechoices.lib.account_adapters.SiteAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_USERNAME_BLACKLIST = SLUG_BLACKLIST
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USERNAME_MIN_LENGTH = "2"
ACCOUNT_USERNAME_VALIDATORS = "routechoices.lib.validators.custom_username_validators"
CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": os.path.join(BASE_DIR, "cache"),
        "TIMEOUT": 300,
        # ^-- Django setting for default timeout of each key.
        "SHARDS": 4,
        "DATABASE_TIMEOUT": 0.10,  # 10 milliseconds
        # ^-- Timeout for each DjangoCache database transaction.
        "OPTIONS": {"size_limit": 2**30},  # 1 gigabyte
    },
}
CACHE_TILES = True
CACHE_THUMBS = True
CACHE_EVENT_DATA = True
AWS_SESSION_TOKEN = ""
AWS_S3_BUCKET = "routechoices"
GEOIP_PATH = os.path.join(BASE_DIR, "geoip")
SILENCED_SYSTEM_CHECKS = ["admin.E410"]
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            "h1",
            "h2",
            "h3",
            "h4",
            "img",
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "em",
            "i",
            "li",
            "ol",
            "p",
            "strong",
            "ul",
            "br",
            "code",
        ],
        "WHITELIST_ATTRS": [
            "href",
            "src",
            "alt",
            "style",
        ],
        "WHITELIST_STYLES": [
            "color",
            "width",
            "height",
            "font-weight",
        ],
    }
}
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    "SCOPES": {"all": "Read and Write data"}
}
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "OAuth2": {
            "type": "oauth2",
            "authorizationUrl": "/oauth2/authorize/",
            "tokenUrl": "/oauth2/token/",
            "flow": "accessCode",
            "scopes": {
                "full": "Read and Write data",
            },
        },
    }
}
XFF_TRUSTED_PROXY_DEPTH = 1
CSP_IMG_SRC = (
    "'self'",
    "*",
    "data:",
    "blob:",
)
CSP_WORKER_SRC = ("'self'", "blob:")
CSP_CHILD_SRC = ("'self'", "blob:")
CSRF_USE_SESSIONS = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [r"^\.well-known/acme-challenge/.+$"]
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": ["self"],
    "geolocation": ["self"],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

try:
    from .settings_overrides import *  # noqa: F403, F401
except ImportError:
    pass
