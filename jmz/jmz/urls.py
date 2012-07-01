from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('maulia.views',
                       url(r'^$', 'index', name='home'),
                       url(r'singly/callback/$', 'connect_to_service', name='home'),
                       url(r'^data/$', 'singly_authorize', name='home'),
                       url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.MEDIA_ROOT}),
                            )
