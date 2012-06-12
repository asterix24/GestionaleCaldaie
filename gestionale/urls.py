from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^home/$', 'main.views.home', name='home'),
    url(r'^anagrafe/$', 'main.views.anagrafe', name='anagrafe'),
    # Generic record
    url(r'^anagrafe/new/$', 'main.views.new_record', name='new_record'),
    url(r'^anagrafe/(?P<record_id>\d+)/edit/$', 'main.views.edit_record', name='edit_record'),
    url(r'^anagrafe/(?P<record_id>\d+)/delete/$', 'main.views.delete_record', name='delete_record'),

    url(r'^anagrafe/new/(?P<record_type>intervento)/$', 'main.views.new_typeRecord', name='new_intervento'),
    url(r'^anagrafe/new/(?P<record_type>bollino)/$', 'main.views.new_typeRecord', name='new_bollino'),
    url(r'^anagrafe/(?P<record_id>\d+)/new/(?P<record_type>intervento)/$', 'main.views.new_typeRecord', name='new_intervento'),
    url(r'^anagrafe/(?P<record_id>\d+)/new/(?P<record_type>bollino)/$', 'main.views.new_typeRecord', name='new_bollino'),
    url(r'^anagrafe/(?P<record_id>\d+)/edit/(?P<record_type>intervento)/(?P<record_type_id>\d+)/$', 'main.views.edit_typeRecord', name='edit_intervento'),
    url(r'^anagrafe/(?P<record_id>\d+)/edit/(?P<record_type>bollino)/(?P<record_type_id>\d+)/$', 'main.views.edit_typeRecord', name='edit_bollino'),
    url(r'^anagrafe/(?P<record_id>\d+)/delete/(?P<record_type>intervento)/(?P<record_type_id>\d+)/$', 'main.views.delete_typeRecord', name='delete_intervento'),
    url(r'^anagrafe/(?P<record_id>\d+)/delete/(?P<record_type>bollino)/(?P<record_type_id>\d+)/$', 'main.views.delete_typeRecord', name='delete_bollino'),


    # Record detail view
    url(r'^anagrafe/(?P<record_id>\d+)/(?P<detail_type>\w+)/$', 'main.views.detail_record', name='detail_record'),

    # url(r'^GestionaleCaldaie/', include('GestionaleCaldaie.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
