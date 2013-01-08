from django.conf.urls.defaults import *
from green.views import current_datetime
#Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from green.views import simple
from green.views import prova, contact

urlpatterns = patterns('',
    # Example:
    # (r'^green/', include('green.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^prova/', simple),
    url(r'^green/', prova),
    url(r'^form/', contact),
    url(r'^contact/', prova),
    url(r'^admin/', include(admin.site.urls)),
)
