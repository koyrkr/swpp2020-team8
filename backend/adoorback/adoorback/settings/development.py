from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

sentry_sdk.init(
    dsn="https://3525cb8e094e49fe9973fd92ccbf456b@o486285.ingest.sentry.io/5543025",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    send_default_pii=True
)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
