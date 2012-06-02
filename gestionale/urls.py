from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'main.views.home', name='home'),
    url(r'^anagrafe/$', 'main.views.anagrafe', name='anagrafe'),
    url(r'^anagrafe/(?P<record_id>\d+)/$', 'main.views.detail_record', name='detail_record'),
    url(r'^anagrafe/(?P<record_id>\d+)/edit/$', 'main.views.edit_record', name='edit_record'),
    url(r'^anagrafe/new/$', 'main.views.new_record', name='new_record'),
    url(r'^anagrafe/edit/(?P<record_id>\d+)/$', 'main.views.test', name='test'),
    
    # url(r'^GestionaleCaldaie/', include('GestionaleCaldaie.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)