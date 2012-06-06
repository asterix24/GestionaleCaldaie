<tr>
    <td class="hdr">Data</td>
    <td>{{ intervento.data|date:"d/m/Y"}}</td>
</tr>
<tr>
    <td class="hdr">Motivo</td>
    <td>{{ intervento.tipo }}</td>
</tr>
<tr>
    <td class="hdr">Rapporto Numero</td>
    <td>{{ intervento.numero_rapporto }}</td>
</tr>
<tr>
    <td class="hdr">Annotazioni</td>
    <td>{{ intervento.note }}</td>
</tr>

{% if intervento.scadenza %}
<tr>
    <td class="hdr">Scade il</td>
    <td>{{ intervento.data_scadenza|date:"d/m/Y" }}</td>
</tr>
<tr>
    <td class="hdr">Stato</td>
    {% if intervento.is_elapse %}
    <td>Valido</td>
    {% else %}
    <td>Scaduto</td>
    {% endif %}
</tr>
{% endif %}
