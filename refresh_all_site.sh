#!/bin/bash

ROOT=gestionale
WSGI=wsgi.py
SITES=('besalba' 'demo')

for t in "${SITES[@]}"
do
	echo -n "touch ${ROOT}/${t}/${WSGI}"
	touch ${ROOT}/${t}/${WSGI}
	echo " ..done"
done
