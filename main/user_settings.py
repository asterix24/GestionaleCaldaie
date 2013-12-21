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


def __settings_ShowHide(settings, key, key_label, default, idx=0):
    settings = settings.values()

    show_settings = default
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

    return {'setting_id':key, 'setting_label':key_label, 'show':show, 'hide':hide}


def settings_home(request):
    items = []
    # get settings from files
    if request.method == "GET":
        settings = models.Settings.objects.all()
        items.append(__settings_ShowHide(settings, 'home_view'    , 'Vista Home',    cfg.HOME_STD_VIEW))
        items.append(__settings_ShowHide(settings, 'anagrafe_view', 'Vista Anagrafe', cfg.HOME_STD_VIEW))
        items.append(__settings_ShowHide(settings, 'export_table' , 'Vista esportazione', cfg.HOME_STD_VIEW))

    return render(request, "user_settings.html", {'items':items})

def settings_view(request):
    print request.POST
    if request.method == "POST":
        form = models.SettingsForm(request.POST)
        select = models.Settings.objects.all()
        if form.is_valid():
            if select:
                v = form.cleaned_data['home_view']
                if v:
                    models.Settings.objects.all().update(home_view=v)
                v = form.cleaned_data['anagrafe_view']
                if v:
                    models.Settings.objects.all().update(anagrafe_view=v)
                v = form.cleaned_data['export_table']
                if v:
                    models.Settings.objects.all().update(export_table=v)
            else:
                form.save()

    return render(request, "user_settings.html", {})

