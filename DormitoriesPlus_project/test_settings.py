"""
Test settings for DormitoriesPlus_project.

This file contains settings specific to testing that override the main settings.
"""

from .settings import *

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use console email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}

# Use faster test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Disable debug mode for tests
DEBUG = False

# Use a simple secret key for tests
SECRET_KEY = 'test-secret-key-for-testing-only'

# Disable CSRF for tests (if needed)
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'csrf' not in middleware.lower()]

# Set test timezone
TIME_ZONE = 'UTC'

# Disable internationalization for tests
USE_I18N = False
USE_L10N = False

# Use static files finder that doesn't require collectstatic
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
]

# Disable media files for tests
MEDIA_ROOT = '/tmp/test_media/'

# Disable template caching for tests
TEMPLATES[0]['OPTIONS']['loaders'] = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
TEMPLATES[0]['APP_DIRS'] = False 