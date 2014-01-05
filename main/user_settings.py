#!/usr/bmport settings
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from main import models
from main import myforms
from main import cfg
from main import tools
from main import data_render
from main import database_manager
from main import scripts
from main import errors

import logging
logger = logging.getLogger(__name__)

def __settings_ShowHide(settings, key, active):
    settings = settings.values()

    show_settings = cfg.cfg_tableList(key)
    # There is a valid user settings, make dict
    if settings:
        # Take last
        settings = settings[0]
        s = settings.get(key, '')
        if s:
            show_settings = s.split('-')
        else:
            logger.error("No custom settings for %s, foldback on default.", key)
    else:
        logger.error("No custom settings for %s, foldback on default.", key)

    show = []
    for i in show_settings:
        show.append({'id':i, 'label': i.replace('_', ' ').capitalize()})

        hide = []
        for i in cfg.CFG_ALL:
            if i not in show_settings:
                hide.append({'id':i, 'label': i.replace('_', ' ').capitalize()})

    return {'setting_id':key, 'setting_label':cfg.cfg_tableLabel(key),
            'show':show, 'hide':hide, 'active':active}


def settings_columView(key):
    select = models.Settings.objects.all()
    l = cfg.cfg_tableList(key)
    if select:
        select = select.values()[0]
        ll = select[key].split('-')
        if ll[0]:
            l = ll
    return l

def settings_reset(request, setting_id):
    if setting_id in cfg.cfg_tableKeys():
        models.Settings.objects.all().update(**{setting_id:''})

    return settings_home(request, setting_id)

def settings_home(request, active=None):
    items = []
    # get settings from files
    if request.method == "GET":
        settings = models.Settings.objects.all()
        for i in cfg.cfg_tableKeys():
            if i == active or active is None:
                items.append(__settings_ShowHide(settings, i, True))
                active = False
                continue

            items.append(__settings_ShowHide(settings, i, False))

    return render(request, "user_settings.html", {'items':items})

def settings_view(request):
    #print request.POST
    if request.method == "POST":
        form = models.SettingsForm(request.POST)
        select = models.Settings.objects.all()
        if form.is_valid():
            if select:
                for i in cfg.cfg_tableKeys():
                    v = form.cleaned_data[i]
                    if v:
                        models.Settings.objects.all().update(**{i:v})
            else:
                form.save()

    return render(request, "user_settings.html", {})



