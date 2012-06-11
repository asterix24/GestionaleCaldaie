from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from main import models
from main import myforms
from main import clienti

def home(request):
    return render(request, 'home.sub', {})

def _diplay_error(request, msg):
    return render(request, 'messages.sub',
        { 'msg_hdr':'Error!',
          'msg_body': msg })

def _diplay_ok(request, msg):
    return render(request, 'messages.sub',
        { 'msg_hdr':'Ok!',
          'msg_body': msg})


def _detail_select(request, record_id, msg='', _type="interventi"):
    cliente = clienti.select_record(models.Cliente.objects, record_id)

    if _type == "interventi":
        data_to_render = clienti.select_interventi(cliente)
    elif _type == "bollini":
        data_to_render = clienti.select_bollini(cliente)
    else:
        return _diplay_error(request, "Detail non sensato..")

    return render(request, 'anagrafe_scheda_' + _type + '.sub',
                    {'top_msg':msg,
                     'cliente': cliente,
                     _type: data_to_render})

def _diplay_scheda(request, record_id, msg=''):
    cliente = clienti.select_record(models.Cliente.objects, record_id)
    bollini = clienti.select_bollini(cliente)
    interventi = clienti.select_interventi(cliente)

    bollini_history = len(bollini)
    if bollini_history >= 1:
        bollini = bollini[0]

    interventi_history = len(interventi)
    if interventi_history >= 1:
        interventi = interventi[0]

    return render(request, 'anagrafe_scheda.sub',
                    {'top_msg':msg,
                     'cliente': cliente,
                     'bollino': bollini,
                     'intervento': interventi,
                     'interventi_history': interventi_history,
                     'bollini_history': bollini_history,
                    })

def detail_record(request, record_id, detail_type = None):
    if record_id == "":
        _diplay_error(request, "Id non trovato.")

    if detail_type == "detail":
        return _diplay_scheda(request, record_id)
    else:
        return _detail_select(request, record_id, '', detail_type)

def edit_record(request, record_id):
    if request.method == 'GET':
        if record_id != "":
            select = clienti.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(instance=select)
            return render(request, 'anagrafe_new.sub', {'action': 'Modifica',
                                                        'record_id': record_id,
                                                        'cliente': form})
        else:
            return _diplay_error(request, "Id non trovato.")

    # We manage a post request when we want to save the data.
    if request.method == 'POST':
        #If we found a id take the record to edit it.
        if record_id != "":
            select = clienti.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(request.POST, instance=select)

            if form.is_valid():
                form.save()
                return _diplay_scheda(request, record_id)
            else:
                return render(request, 'anagrafe_new.sub', {'action': 'Modifica',
                                                        'record_id': record_id,
                                                        'cliente': form})
        else:
            return _diplay_error(request, "Id non trovato.")

def new_record(request):
    if request.method == 'GET':
        form = models.ClienteForm()
        return render(request, 'anagrafe_new.sub', {'action': 'Nuovo',
                                                'cliente': form})
    if request.method == 'POST':
        form = models.ClienteForm(request.POST)
        if form.is_valid():
            istance = form.save()
            s = "Cliente: %s %s aggiunto correttamente." % (request.POST.get('nome'), request.POST.get('cognome'))
            return _diplay_scheda(request, istance.id, s)
        else:
            return render(request, 'anagrafe_new.sub', {'action': 'Nuovo',
                                                    'cliente': form})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def delete_record(request, record_id):
    try:
        if request.method == 'GET':
            return render(request, 'anagrafe_delete.sub', {'record_id':record_id,
                                                           'cliente': clienti.select_record(models.Cliente.objects, record_id)})

        if request.method == 'POST':
            cli = clienti.select_record(models.Cliente.objects, record_id)
            nome = cli.nome
            cognome = cli.cognome
            cli.delete()
            s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)
            return _diplay_ok(request, s)

    except ObjectDoesNotExist, m:
        return _diplay_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _diplay_error(request, "Qualcosa e' andato storto..")


def edit_intervento(request, record_id, intervento_id = None):
    if request.method == 'GET':
        if intervento_id is not None:
            form = models.InterventoForm(instance = clienti.select_interventi(models.Intervento.objects, intervento_id))
        else:
            form = models.InterventoForm()

        return render(request, 'record_type_mgr.sub', {'action': 'Modifica',
                                                      'intervento': form,
                                                      'record_id': record_id,
                                                      'intervento_id': intervento_id})

    if request.method == 'POST':
        if intervento_id is not None:
            print "qui..", intervento_id
            form = models.InterventoForm(request.POST, instance=clienti.select_interventi(models.Intervento.objects, intervento_id))
        else:
            form = models.InterventoForm(request.POST)

        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()
            return _diplay_scheda(request, record_id, "L'intervento del %s e' stato modificato correttamente." %
                                                                form.cleaned_data['data'].strftime("%d/%m/%y"))
        else:
            return render(request, 'record_type_mgr.sub', {'action': 'Modifica',
                                                          'intervento': form,
                                                          'record_id': record_id,
                                                          'intervento_id': intervento_id})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def delete_intervento(request, record_id, intervento_id = None):
    try:
        if request.method == 'GET':
            return render(request, 'intervento_delete.sub', {'action': 'Modifica',
                                                             'intervento': clienti.select_interventi(models.Intervento.objects, intervento_id),
                                                             'record_id': record_id,
                                                             'intervento_id': intervento_id})
        if request.method == 'POST':
            inter = clienti.select_interventi(models.Intervento.objects, intervento_id)
            try:
                data = inter.data.strftime("%d/%m/%y")
            except ValueError:
                data = ""

            tipo = models.interventi_choicesExteded(inter.tipo)
            inter.delete()
            return _diplay_scheda(request, record_id, "Intervento \"%s\" del %s, Rimosso correttamente." % (tipo, data))

    except ObjectDoesNotExist, m:
        return _diplay_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _diplay_error(request, "Qualcosa e' andato storto..")



def new_typeRecord(request, record_id = None, record_type = None):
    if record_type is None:
        return _diplay_error(request, "Qualcosa e' andato storto..")

    if request.method == 'GET':
        if record_id is None:
            if record_type == "intervento":
                form = models.InterventoForm()
            else:
                form = models.BollinoForm()
        else:
            if record_type == "intervento":
                form = models.InterventoForm(initial={'cliente': clienti.select_record(models.Cliente.objects, record_id)})
            else:
                form = models.BollinoForm(initial={'cliente': clienti.select_record(models.Cliente.objects, record_id)})

        # TODO: cambiare il nome..
        return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                      'form': form,
                                                      'record_id': record_id,
                                                      'record_type': record_type })

    if request.method == 'POST':
        if record_type == "intervento":
            form = models.InterventoForm(request.POST)
        else:
            form = models.BollinoForm(request.POST)

        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()
            if record_type == "intervento":
                s = "L\'intervento \"%s\" del %s e' stato aggiunto correttamente." % (models.interventi_choicesExteded(form.cleaned_data['tipo']), form.cleaned_data['data'].strftime("%d/%m/%y"))
            else:
                s = "Il Bollino e' stato aggiunto correttamente."

            return _diplay_scheda(request, record_id, s)
        else:
            # TODO: cambiare il nome..
            return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                          'form': form,
                                                          'record_id': record_id,
                                                          'record_type': record_type })

    return _diplay_error(request, "Qualcosa e' andato storto..")

def new_intervento(request, record_id = None):
    if request.method == 'GET':
        if record_id is None:
            form = models.InterventoForm()
        else:
            form = models.InterventoForm(initial={'cliente': clienti.select_record(models.Cliente.objects, record_id)})

        return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                      'intervento': form,
                                                      'record_id': record_id })

    if request.method == 'POST':
        form = models.InterventoForm(request.POST)
        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()
            return _diplay_scheda(request, record_id, "L'intervento \"%s\" del %s e' stato aggiunto correttamente." %
                            (models.interventi_choicesExteded(form.cleaned_data['tipo']), form.cleaned_data['data'].strftime("%d/%m/%y")))
        else:
            return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                          'intervento': form,
                                                          'record_id': record_id})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def new_bollino(request, record_id = None):
    if request.method == 'GET':
        if record_id is None:
            form = models.BollinoForm()
        else:
            form = models.BollinoForm(initial={'cliente': clienti.select_record(models.Cliente.objects, record_id)})

        return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                    'intervento': form,
                                                    'record_id': record_id })

    if request.method == 'POST':
        form = models.BollinoForm(request.POST)
        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()
            return _diplay_scheda(request, record_id, "L'bollino \"%s\" del %s e' stato aggiunto correttamente." %
                            (models.interventi_choicesExteded(form.cleaned_data['tipo']), form.cleaned_data['data'].strftime("%d/%m/%y")))
        else:
            return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                          'intervento': form,
                                                          'record_id': record_id})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def edit_bollino(request, record_id, bollino_id = None):
    if request.method == 'GET':
        if bollino_id is not None:
            form = models.BollinoForm(instance = clienti.select_interventi(models.Bollino.objects, bollino_id))
        else:
            form = models.BollinoForm()

        return render(request, 'record_type_mgr.sub', {'action': 'Modifica',
                                                      'intervento': form,
                                                      'record_id': record_id,
                                                      'intervento_id': bollino_id})

    if request.method == 'POST':
        if bollino_id is not None:
            form = models.BollinoForm(request.POST, instance=clienti.select_interventi(models.Bollino.objects, bollino_id))
        else:
            form = models.BollinoForm(request.POST)

        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()
            return _diplay_scheda(request, record_id, "L'bollino del %s e' stato modificato correttamente." %
                                                                form.cleaned_data['data'].strftime("%d/%m/%y"))
        else:
            return render(request, 'bollino_mgr.sub', {'action': 'Modifica',
                                                          'bollino': form,
                                                          'record_id': record_id,
                                                          'bollino_id': bollino_id})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def delete_bollino(request, record_id, bollino_id = None):
    try:
        if request.method == 'GET':
            return render(request, 'bollino_delete.sub', {'action': 'Modifica',
                                                             'bollino': clienti.select_interventi(models.Bollino.objects, bollino_id),
                                                             'record_id': record_id,
                                                             'bollino_id': bollino_id})
        if request.method == 'POST':
            inter = clienti.select_interventi(models.Bollino.objects, bollino_id)
            try:
                data = inter.data.strftime("%d/%m/%y")
            except ValueError:
                data = ""

            tipo = models.interventi_choicesExteded(inter.tipo)
            inter.delete()
            return _diplay_scheda(request, record_id, "bollino \"%s\" del %s, Rimosso correttamente." % (tipo, data))

    except ObjectDoesNotExist, m:
        return _diplay_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _diplay_error(request, "Qualcosa e' andato storto..")




def anagrafe(request):
    form = myforms.FullTextSearchForm()

    if request.method == 'GET' and request.GET != {}:
        form = myforms.FullTextSearchForm(request.GET)
        if form.is_valid():
            data_to_render = clienti.search_fullText(models.Cliente.objects, form.cleaned_data['s'])
        else:
            """stringa vuota faccio vedere tutto"""
            form = myforms.FullTextSearchForm()
            data_to_render = clienti.clienti_displayAll(models.Cliente.objects)

        return render(request, 'anagrafe.sub',
            {'clienti': data_to_render,
             'display_data':1,
             'display_search_bot':1,
             'form': form })

    return render(request, 'anagrafe.sub', {'display_data':0,
                                        'display_search_bot':0,
                                        'form': form })
