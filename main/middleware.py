#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings

class LoginRequiredMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated() and request.path_info != settings.LOGIN_URL:
            return HttpResponseRedirect(settings.LOGIN_URL)





