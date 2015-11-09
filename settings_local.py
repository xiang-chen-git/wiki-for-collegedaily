# global settings for this school
DEBUG = True

SITE_ROOT = '/home/jiaqing/webapps/admin_campus/'
MEDIA_ROOT = SITE_ROOT + 'media/'

STATICFILES_DIRS = (
    SITE_ROOT + 'static/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
TEMPLATE_DIRS = (
    SITE_ROOT + 'templates/',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
