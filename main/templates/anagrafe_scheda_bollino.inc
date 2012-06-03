
<tr>
    <td class="hdr">Storico</td>
    <td><a href="">{{ history_bollini_len }}</a></td>
</tr>
<tr>
    <td class="hdr">Data</td>
    <td>{{ bollino.data|date:"d/m/Y"}}</td>
</tr>
<tr>
    <td class="hdr">Numero</td>
    <td>{{ bollino.numero_bollino }}</td>
</tr>
<tr>
    <td class="hdr">Colore</td>
    <td>{{ bollino.colore }}</td>
</tr>
<tr>
    <td class="hdr">Valore</td>
    <td>{{ bollino.valore }}&euro;</td>
</tr>
<tr>
    <td class="hdr">Scadenza</td>
    <td>{{ bollino.scadenza|date:"d/m/Y"}}</td>
</tr>
<tr>
    <td class="hdr">Note</td>
    <td>{{ bollino.note }}</td>
</tr>
