#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

def render_item(item, fill_string, header=False):
    content = ""
    for f in item._meta.fields:
        # resolve picklists/choices, with get_xyz_display() function
        get_choice = 'get_'+f.name+'_display'
        if hasattr(item, get_choice):
            value = getattr(item, get_choice)()
        else:
            try :
                value = getattr(item, f.name)
            except ObjectDoesNotExist:
                value = None

        # only display fields with values and skip some fields entirely
        if f.editable and value and f.name not in ('id', 'status', 'workshop', 'user', 'complete'):
            if not header:
                string = value
                if f.name in ('nome', 'cognome'):
                    string = "<a href=\"/anagrafe/%s/detail\">%s</a>" % (item.pk, value)

                content += fill_string % string
            else:
                content += fill_string % f.verbose_name.capitalize()

    return content

def render_toTable(items):
    cycle = False
    display_header = True

    table = "<table id=\"customers\">"
    for item in items:
        if display_header:
            table += render_item(item, "<th>%s</th>", header=True)
            display_header = False

        cycle_str = ""
        if cycle:
            cycle_str = " class=\"alt\""
        cycle = not cycle

        table += "<tr%s>" % cycle_str
        table += render_item(item, "<td>%s</td>", header=False)
        table += "</tr>"

    table += "</table>"

    return table

