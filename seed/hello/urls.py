from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hello.views.home', name='home'),
    # url(r'^hello/', include('hello.foo.urls')),
    url(r'^$', 'wiki.views.index', name='index'),
    url(r'^ua/', include('account.urls', namespace='ua')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wiki/', include('wiki.urls', namespace='wiki')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

