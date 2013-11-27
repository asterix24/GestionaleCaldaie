from django.conf.urls.defaults import patterns, include, url
handler500 = 'main.errors.server_error'
handler404 = 'main.errors.page_not_found'
handler403 = 'main.errors.permission_denied_view'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # login
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url':'/login/'}),

	url(r'^$', 'main.views.home', name='home'),
	url(r'^home/$', 'main.views.home', name='home'),
	#url(r'^maps/$', 'main.views.maps', name='maps'),
	url(r'^export/anagrafe/$', 'main.views.export_csv', name='expor_csv'),
	url(r'^anagrafe/$', 'main.anagrafe.anagrafe', name='anagrafe'),

	# Client manager urls
	url(r'^anagrafe/add/$', 'main.anagrafe.add_record', name='add_record'),
	url(r'^anagrafe/(?P<cliente_id>\d+)/$', 'main.anagrafe.detail_record', name='detail_record'),
	url(r'^anagrafe/(?P<cliente_id>\d+)/edit/$', 'main.anagrafe.edit_record', name='edit_record'),
	url(r'^anagrafe/(?P<cliente_id>\d+)/delete/$', 'main.anagrafe.delete_record', name='delete_record'),

	# Impianti manager urls
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/add/$', 'main.anagrafe.add_record', name='add_record'),
	# Add new Impianto to existing Cliente
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/(?P<impianto_id>\d+)/add/$', 'main.anagrafe.add_record', name='add_record'),
	# Add new Verifica/Interventi to existing Impianto
	url(r'^anagrafe/(?P<cliente_id>\d+)/impianto/(?P<impianto_id>\d+)/(?P<detail_type>\w+)/add/$', 'main.anagrafe.add_record', name='add_record'),

	# Delete Impianti
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/(?P<impianto_id>\d+)/delete/$', 'main.anagrafe.delete_record', name='delete_record'),
	# Delete verifica/interventi
	#/anagrafe/356/impianto/762/verifica/758/delete/
	url(r'^anagrafe/(?P<cliente_id>\d+)/impianto/(?P<impianto_id>\d+)/(?P<detail_type>\w+)/(?P<sub_impianto_id>\d+)/delete/$', 'main.anagrafe.delete_record', name='delete_record'),
	# Show Impianti detail of select Cliente
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/(?P<impianto_id>\d+)/$', 'main.anagrafe.detail_record', name='detail_record'),
	# Show Verifica/Interventi detail of select Impianti
	url(r'^anagrafe/(?P<cliente_id>\d+)/impianto/(?P<impianto_id>\d+)/(?P<detail_type>\w+)/(?P<sub_impianto_id>\d+)/$', 'main.anagrafe.detail_record', name='detail_record'),

	# /anagrafe/356/impianto/760/edit/
	url(r'^anagrafe/(?P<cliente_id>\d+)/(?P<detail_type>\w+)/(?P<impianto_id>\d+)/edit/$', 'main.anagrafe.edit_record', name='edit_record'),
	# /anagrafe/356/impianto/760/verifica/1/edit/
	url(r'^anagrafe/(?P<cliente_id>\d+)/impianto/(?P<impianto_id>\d+)/(?P<detail_type>\w+)/(?P<sub_impianto_id>\d+)/edit/$', 'main.anagrafe.edit_record', name='edit_record'),

    #settings
	url(r'^settings/$', 'main.user_settings.slide_list', name='slide_list'),

	# Uncomment the admin/doc line below to enable admin documentation:
	#url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),

	#url(r'^err/$', 'main.views.err', name='err'),
	#url(r'^dev/populatedb/$', 'main.views.populatedb', name='populat_db'),
	#url(r'^test/(?P<search_string>\w+)/$', 'main.views.test', name='test'),
	#url(r'^check_test/$', 'main.views.check_test', name='check_test'),
	#url(r'^layout/$', 'main.views.check_layout', name='check_layout'),
)
