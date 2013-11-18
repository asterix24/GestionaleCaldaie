#!/bin/bash
set -x

if [ $# -lt 2 ]; then
	echo -e $0 "<site_name> <site_name_log>"
	exit 1;
fi

NEW_SITE=$1
NEW_SITE_LONG=$2
SETTING_DIR="gestionale"
DEFAULT="$SETTING_DIR/default"
NEW=$SETTING_DIR/$NEW_SITE
CURRENT_DIR=`pwd`
DB_GEN_PASS=`tr -dc A-Za-z0-9_ < /dev/urandom | head -c 16 | xargs`

cp -r $DEFAULT $NEW
sed -i "s/DEFAULT/$NEW_SITE/g" $NEW/local_settings.py
sed -i "s/DEFAULT_LONG/$NEW_SITE_LONG/g" $NEW/local_settings.py
sed -i "s/DB_NAME/${NEW_SITE}_gestionale/g" $NEW/local_settings.py
sed -i "s/DB_USER/$NEW_SITE/g" $NEW/local_settings.py
sed -i "s/DB_PASS/$DB_GEN_PASS/g" $NEW/local_settings.py
sed -i "s,PWD,$CURRENT_DIR,g" $NEW/local_settings.py

sed -i "s/DEFAULT/$NEW_SITE/g" $NEW/wsgi.py

mkdir "main/data/$NEW_SITE"

mkdir "main/templates/$NEW_SITE"
mkdir "main/static/$NEW_SITE"
ln -s /home/asterix/venv/lib/python2.7/site-packages/Django-1.4-py2.7.egg/django/contrib/admin/static/admin/ main/static/$NEW_SITE/admin
ln -s ../common main/static/$NEW_SITE/common

mkdir "log/$NEW_SITE"
mkdir "html/$NEW_SITE"
touch "html/$NEW_SITE/favicon.ico"

cat <<EOF >> gestionale/__init__.py
if os.environ["DJANGO_SETTINGS_MODULE"] == "gestionale.${NEW_SITE}.settings":
    from ${NEW_SITE} import local_settings
    from ${NEW_SITE} import settings
    from ${NEW_SITE}.local_settings import local_env
EOF
