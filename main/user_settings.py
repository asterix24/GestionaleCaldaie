#!/usr/bmport settings
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from main import models
from main import cfg
from main import scripts

import logging
logger = logging.getLogger(__name__)

def __settings_ShowHide(settings, key, default, idx=0):
    settings = settings.values()
    show = default
    hide = []
    if idx == len(settings) and idx > 0:
        idx = idx - 1

    if settings:
        settings = settings[idx]
        s = settings.get(key, '')
        if s:
            show = s.split('-')
        else:
            logger.error("No custom settings for %s, foldback on default.", key)
    else:
        logger.error("No custom settings for %s, foldback on default.", key)

    for i in cfg.CFG_ALL:
        if i in show:
            continue
        hide.append(i)

    return show, hide

def settings_home(request):
    home_view_show = []
    home_view_hide = []

    # get settings from files
    if request.method == "GET":
        settings = models.Settings.objects.all()
        home_view_show, home_view_hide = __settings_ShowHide(settings, 'home_view', cfg.HOME_STD_VIEW)

    return render(request, "settings.sub", { 'home_show':home_view_show, 'home_hide':home_view_hide})

def settings_view(request):
    if request.method == "POST":
        print request.POST
        try:
            select = models.Settings.objects.get(pk=0)
        except ObjectDoesNotExist:
            select = None

        form = models.SettingsForm(request.POST, instance=select)
        if form.is_valid():
            form.save()

    return http.HttpResponse()


