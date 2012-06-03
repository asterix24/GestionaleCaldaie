<tr>
    <td class="hdr">Storico</td>
    <td><a href="">{{ history_interventi_len }}</a></td>
</tr>
<tr>
    <td class="hdr">Ultimo interverto</td>
    <td>{{ intervento.data|date:"d/m/Y"}}</td>
</tr>
<tr>
    <td class="hdr">Motivo dell'intervento</td>
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
{% endif %}
