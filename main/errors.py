#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render

def server_error(request):
    return render(request, 'messages.sub',{'msg_hdr':'Qualcosa è andato storto!' })

def page_not_found(request):
    return render(request, 'messages.sub',{'msg_hdr':'Pagina non trovata!' })

def permission_denied_view(request):
    return render(request, 'messages.sub',{'msg_hdr':'Permesso negato.' })
