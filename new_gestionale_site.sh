#!/bin/bash
set -x

if [ $# -lt 1 ]; then
	echo -e $0 "<site_name>"
	exit 1;
fi

NEW_SITE=$1
SETTING_DIR="gestionale"
DEFAULT="$SETTING_DIR/default"
NEW=$SETTING_DIR/$NEW_SITE
CURRENT_DIR=`pwd`

cp -r $DEFAULT $NEW
sed -i "" "s/DEFAULT/$NEW_SITE/g" $NEW/local_settings.py
sed -i "" "s/DEFAULT/$NEW_SITE/g" $NEW/wsgi.py
sed -i "" "s,PWD,$CURRENT_DIR,g" $NEW/local_settings.py

mkdir "main/templates/$NEW_SITE"
