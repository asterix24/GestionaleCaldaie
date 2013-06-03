#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings

class LoginRequiredMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated() and request.path_info != settings.LOGIN_URL:
            return HttpResponseRedirect(settings.LOGIN_URL)

from django.contrib.auth import logout
from django.contrib import messages
import datetime

class SessionIdleTimeout:
    """Middleware class to timeout a session after a specified time period.
    """
    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and \
                (current_datetime - request.session['last_activity']).seconds > \
                settings.SESSION_IDLE_TIMEOUT:
                logout(request)
                messages.add_message(request, messages.ERROR, 'La sessione e\' scaduta.')
            # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime
        return None




