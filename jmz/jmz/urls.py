from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('maulia.views',
                       url(r'^$', 'connect_to_service', name='home'),
                       url(r'^singly/callback/$', 'singly_authorize', name='home'),
                       url(r'^admin/', include(admin.site.urls)),
)
