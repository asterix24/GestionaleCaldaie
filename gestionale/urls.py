from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^test/', 'main.views.test', name='test'),
    url(r'^edit/', 'main.views.edit', name='edit'),
    url(r'^anagrafe/', 'main.views.anagrafe', name='anagrafe'),
    url(r'^scheda/', 'main.views.scheda_cliente', name='scheda_cliente'),

    # url(r'^GestionaleCaldaie/', include('GestionaleCaldaie.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
