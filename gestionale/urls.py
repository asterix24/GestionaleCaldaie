from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^home/$', 'main.views.home', name='home'),

    url(r'^anagrafe/$', 'main.views.anagrafe', name='anagrafe'),

    # Client manager urls
    url(r'^anagrafe/add/$', 'main.views.add_record', name='add_record'),
    url(r'^anagrafe/(?P<cliente_id>\d+)/$', 'main.views.detail_record', name='detail_record'),
    url(r'^anagrafe/(?P<cliente_id>\d+)/edit/$', 'main.views.edit_record', name='edit_record'),
    url(r'^anagrafe/(?P<cliente_id>\d+)/delete/$', 'main.views.delete_record', name='delete_record'),

    # Impianti manager urls
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/add/$', 'main.views.add_record', name='add_record'),
    # Add new Impianto to existing Cliente
    url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/(?P<impianto_id>\d+)/add/$', 'main.views.add_record', name='add_record'),
    # Add new Verifiche/Interventi to existing Impianto
    url(r'^anagrafe/(?P<cliente_id>\d+)/impianto/(?P<impianto_id>\d+)/(?P<detail_type>\w+)/add/$', 'main.views.add_record', name='add_record'),

    # Show Impianti detail of select Cliente
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/(?P<impianto_id>\d+)/$', 'main.views.detail_record', name='detail_record'),
    # Show Verifiche/Interventi detail of select Impianti
	url(r'^anagrafe/(?P<cliente_id>\d+)/impianto/(?P<impianto_id>\d+)/(?P<detail_type>\w+)/(?P<sub_impianto_id>\d+)/$', 'main.views.detail_record', name='detail_record'),


    #url(r'^anagrafe/(?P<record_id>\d+)/(?P<detail_type>\w+)/(?P<sub_record_id>\d+)/delete/$', 'main.views.delete_record', name='delete_record'),
	#url(r'^anagrafe/(?P<record_id>\d+)/(?P<detail_type>\w+)/(?P<sub_record_id>\d+)/edit/$', 'main.views.edit_record', name='edit_record'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

	url(r'^dev/populatedb/$', 'main.views.populatedb', name='populat_db'),
)
