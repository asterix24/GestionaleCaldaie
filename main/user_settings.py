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


def __settings_ShowHide(settings, key, default, idx=0):
    settings = settings.values()
    show = default
    hide = []

    #TODO Rivedere un po'
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
    return render(request, "user_settings.sub", { })

def slide_list(request):
    home_view_show = []
    home_view_hide = []

    # get settings from files
    if request.method == "GET":
        settings = models.Settings.objects.all()
        home_view_show, home_view_hide = __settings_ShowHide(settings, 'home_view', cfg.HOME_STD_VIEW)

    if request.method == "POST":
        try:
            select = models.Settings.objects.get(pk=0)
        except ObjectDoesNotExist:
            select = None

        form = models.SettingsForm(request.POST, instance=select)
        if form.is_valid():
            form.save()
    return render(request, "user_settings.sub", { 'home_show':home_view_show, 'home_hide':home_view_hide})

