#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


DELETE = 'delete'
EDIT = 'edit'
ADD = 'add'
ALL = 'all'

def hasPermission(request, type=ALL):
    if request.user.groups.filter(name=ALL):
        return True

    if request.user.groups.filter(name=type):
        return True

    return False

def has_deletePermission(request):
    if hasPermission(request, DELETE):
        return True

    return False

def has_addPermission(request, select):
    if (select is None) and hasPermission(request, ADD):
        return True

    return False

def has_editPermission(request, select):
    if (select is not None) and hasPermission(request, EDIT):
        return True

    return False

