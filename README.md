GestionaleCaldaie
=================

Piccolo gestionale per la gestione dei cliente e delle manutenzioni programmate
delle caldaie, scritto in python e Django



Per aggiungere un nuovo sito
============================

- preparare le cartelle di django con lo script
- verificare che tutto é al suo posto
- controllare anche se il link ad admin c'è nelle relative cartelle
- aggiungere un nuovo virtual host:

"""
<VirtualHost *:80>
    ServerName demo.gestioneimpianti.net
    ServerAdmin asterix24@gmail.com

    ErrorLog /home/asterix/gestionale_www/log/demo/error.log
    CustomLog /home/asterix/gestionale_www/log/demo/access.log combined

    WSGIDaemonProcess demo.gestioneimpianti.net user=asterix python-path=/home/asterix/venv/local/lib/python2.7/:/home/asterix/gestionale_www/ display-name=%{GROUP}
    WSGIProcessGroup demo.gestioneimpianti.net
    WSGIScriptAlias / /home/asterix/gestionale_www/gestionale/demo/wsgi.py

    <Directory />
	Options FollowSymLinks
        AllowOverride None
    </Directory>

    Alias /robots.txt /home/asterix/gestionale_www/html/demo/robots.txt
    Alias /favicon.ico /home/asterix/gestionale_www/html/demo/favicon.ico
    Alias /static/ /home/asterix/gestionale_www/main/static/demo/

    <Directory /home/asterix/gestionale_www/main/static/demo>
    Order deny,allow
    Allow from all
    </Directory>

    <Directory /home/asterix/gestionale_www/html/demo>
    Order deny,allow
    Allow from all
    </Directory>

    <Directory /home/asterix/gestionale_www/gestionale>
    <Files wsgi.py>
        Order deny,allow
        Allow from all
    </Files>
         Options Indexes FollowSymLinks MultiViews
	 AllowOverride None
	 Order allow,deny
	 allow from all
    </Directory>
</VirtualHost>
"""

abilitare il nuovo script:
$ a2ensite demo-gestioneimpianti.net
riavviare apache
$ service apache2 reload

- Fatto questo aggiungere le nuove tabelle e utente a postgress:
- Modificare questo file:
 vi /etc/postgresql/9.1/main/pg_hba.conf

"""
# LXC: container access
host     gestionale          asterix              192.168.10.101    255.255.255.0    md5
host     demo_gestionale     demo                 192.168.10.101    255.255.255.0    md5
"""
l'indirizzo riportato qui sopra deve essere lo stesso di quello del file di configurazione

- Ricaricare psql:

$ /etc/init.d/postgresql reload

- Generare il nuovo schema:
$ ../venv/bin/python manage.py syncdb --settings="gestionale.demo.settings"

- Creare le nuove migrazioni:
$ ../venv/bin/python manage.py schemamigration main --initial --settings="gestionale.demo.settings"
e applicarle
$
e applicarle
$ ../venv/bin/python manage.py migrate main --settings="gestionale.demo.settings" --fake

usare il fake se non funziona.


- Per la prima volta aggiungere nel panello di admin i gruppi per i permessi:
   - all: tutti i permessi
   - edit: solo i permessi di modifica
   - delete: solo i permessi di cancellazione
   - add: solo i permessi di aggiunta

Per i super user utilizzare 'all'

