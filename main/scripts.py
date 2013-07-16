#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOME_ADD_JS = """
<script>
$("input[type=button]").click( function() {
    var button_action = $(this).val();
    if (button_action == 'Seleziona Tutti') {
        $("input[name=row_select]").attr('checked', true);
        $(this).val('Deseleziona Tutti');
    } else if (button_action == 'Deseleziona Tutti') {
        $("input[name=row_select]").attr('checked', false);
        $(this).val('Seleziona Tutti');
    }
});
</script>
"""

MAPS_ADD_JS = """
<script>
var mapOptions = {
  center: new google.maps.LatLng(-34.397, 150.644),
  zoom: 8,
  mapTypeId: google.maps.MapTypeId.ROADMAP
};

var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

var myLatLng = new google.maps.LatLng(-33.890542, 151.274856);

var beachMarker = new google.maps.Marker({
    position: myLatLng,
    map: map
})

</script>
"""

SHOW_ADD_JS = """
<script>

</script>
"""

EDIT_ADD_JS = """
<script>

</script>
"""

ANAGRAFE_JS = """
<script>
$("a[id=toolbar_delete]").click(function(event) {
    event.preventDefault();
    $("#notification_hdr").text('Attenzione!');
    $("#notification_body").text($(this).attr('value'));
    $("#notification_btn").text('Cancella ' + $(this).attr('name'));
    $("#notification_act").attr('action', $(this).attr('href'));
    $("#notification_area").modal('show');
});
</script>
"""


__IMPIANTO_ADD_JS = """
<script>
%s

$("#tr_altra_potenza_caldaia").hide();
otherField($("#id_potenza_caldaia option:selected"), $("#id_potenza_caldaia"), $("#id_altra_potenza_caldaia"));

$("#tr_altro_tipo_caldaia").hide();
otherField($("#id_tipo_caldaia option:selected"), $("#id_tipo_caldaia"), $("#id_altro_tipo_caldaia"));

$("#id_potenza_caldaia").change(function () {
    otherField($("#id_potenza_caldaia option:selected"), $("#id_potenza_caldaia"), $("#id_altra_potenza_caldaia"))
    });

$("#id_tipo_caldaia").change(function () {
    otherField($("#id_tipo_caldaia option:selected"), $("#id_tipo_caldaia"), $("#id_altro_tipo_caldaia"));
    });

$("#id_data_installazione").datepicker({
    showButtonPanel: true,
    dateFormat: "dd/mm/yy",
    currentText: "Oggi",
    closeText: "Chiudi",
    dayNames: [ "Domenica", "Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato" ],
    dayNamesShort: [ "Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab" ],
    monthNames: [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ],
    monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ],
});

$("#id_data_contratto").datepicker({
    showButtonPanel: true,
    dateFormat: "dd/mm/yy",
    currentText: "Oggi",
    closeText: "Chiudi",
    dayNames: [ "Domenica", "Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato" ],
    dayNamesShort: [ "Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab" ],
    monthNames: [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ],
    monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ],
});
</script>
"""

__VERIFICA_ADD_JS = """
<script>
%s
$("div[id=radio_fmt]").buttonset();

if($("#id_tipo_verifica").val() != "provafumi") {
    $("#tr_colore_bollino").hide();
    $("#tr_numero_bollino").hide();
    $("#tr_valore_bollino").hide();
    $("#tr_prossima_analisi_combustione").hide();
    $("#tr_scadenza_fumi_tra").hide();
}

$("#tr_altro_tipo_verifica").hide();
otherField($("#id_tipo_verifica option:selected"), $("#id_tipo_verifica"), $("#id_altro_tipo_verifica"));


var potenza_caldaia = $("#td_potenza_caldaia").text();
var colore_bollino = "Blu";

if (potenza_caldaia == "C1") {
    colore_bollino = "Blu";
} else if (potenza_caldaia == "C2") {
    colore_bollino = "Giallo";
} else {
    colore_bollino = "Arancio";
}

$("#id_colore_bollino option").each(function() {
    if($(this).text() == colore_bollino) {
        $(this).attr('selected', 'selected');
    }
});

$("#tr_altro_colore_bollino").hide();
otherField($("#id_colore_bollino option:selected"), $("#id_colore_bollino"), $("#id_altro_colore_bollino"));

$("#id_data_verifica").datepicker({
    showButtonPanel: true,
    dateFormat: "dd/mm/yy",
    currentText: "Oggi",
    closeText: "Chiudi",
    dayNames: [ "Domenica", "Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato" ],
    dayNamesShort: [ "Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab" ],
    monthNames: [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ],
    monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ],
    onSelect: function(dateText) {
        $('#id_prossima_verifica').val(addMonth(dateText, 12));
    }
});

$("#id_scadenza_verifica_tra").keyup(function () {
    this.value = this.value.replace(/[^0-9\.]/g,'');
    if ($(this).val()) {
        $('#id_prossima_verifica').val(addMonth($("#id_data_verifica").val(), parseInt($(this).val())));
    } else {
        $('#id_prossima_verifica').val($('#id_data_verifica').val());
    }
}).keyup();

$('#id_prossima_verifica').datepicker({
    showButtonPanel: true,
    dateFormat: "dd/mm/yy",
    currentText: "Oggi",
    closeText: "Chiudi",
    dayNames: [ "Domenica", "Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato" ],
    dayNamesShort: [ "Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab" ],
    monthNames: [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ],
    monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ],
});


$("#id_tipo_verifica").change(function () {
    var str = "";
    $("#id_tipo_verifica option:selected").each(function () {
        if ($(this).text() == "Altro..") {
            $("#id_tipo_verifica").parent().append($("#id_altro_tipo_verifica"));
            $("#id_altro_tipo_verifica").show("slow");
        } else if ($(this).text() == "Verde") {
            $("#id_scadenza_fumi_tra").val("12");
        } else {
            $("#id_altro_tipo_verifica").hide();
        }
    });
});


$("#id_colore_bollino").change(function () {
    var scadenza_mesi = 24;
    var colore_bollino_sel = $("#id_colore_bollino option:selected").val()
    if (colore_bollino_sel  == "altro") {
        $("#id_colore_bollino").parent().append($("#id_altro_colore_bollino"));
        $("#id_altro_colore_bollino").show("slow");
    } else if (colore_bollino_sel == "blu") {
        scadenza_mesi = 24;
    } else if (colore_bollino_sel == "verde") {
        if (deltaYear($("#td_data_installazione").text()) > 8) {
            scadenza_mesi = 24;
        } else {
            if ($("#td_tipo_caldaia").text() == "C") {
                scadenza_mesi = 48;
            }
        }
    } else if (colore_bollino_sel == "arancione") {
        scadenza_mesi = 12;
    } else if (colore_bollino_sel == "giallo") {
        scadenza_mesi = 12;
    } else {
        $("#id_altro_colore_bollino").hide();
    }
    $("#id_scadenza_fumi_tra").val(scadenza_mesi);
    $('#id_prossima_analisi_combustione').val(addMonth($("#id_data_verifica").val(), scadenza_mesi));
});

$("#id_tipo_verifica").change( function() {
    if ($(this).val() == "provafumi") {
        $("#tr_colore_bollino").show("slow");
        $("#tr_numero_bollino").show("slow");
        $("#tr_valore_bollino").show("slow");
        $("#tr_prossima_analisi_combustione").show("slow");
        $("#tr_scadenza_fumi_tra").show("slow");
    } else {
        $("#tr_valore_bollino").slideUp();
        $("#tr_numero_bollino").slideUp();
        $("#tr_colore_bollino").slideUp();
        $("#tr_prossima_analisi_combustione").slideUp();
        $("#tr_scadenza_fumi_tra").slideUp();
    }
});

$('#id_prossima_analisi_combustione').datepicker({
    showButtonPanel: true,
    dateFormat: "dd/mm/yy",
    currentText: "Oggi",
    closeText: "Chiudi",
    dayNames: [ "Domenica", "Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato" ],
    dayNamesShort: [ "Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab" ],
    monthNames: [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ],
    monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ],
});

$("#id_scadenza_fumi_tra").keyup(function () {
    this.value = this.value.replace(/[^0-9\.]/g,'');
    if ($(this).val()) {
        $('#id_prossima_analisi_combustione').val(addMonth($("#id_data_verifica").val(), parseInt($(this).val())));
    } else {
        $('#id_prossima_analisi_combustione').val($('#id_data_verifica').val());
    }
}).keyup();
</script>
"""

__INTERVENTO_ADD_JS = """
<script>
%s
</script>
"""

COMMON_FUNCTION = """
function otherField(id_select, id_combobox, id_other) {
    if (id_select.val() == "altro") {
        id_combobox.parent().append(id_other);
        id_other.show("slow");
    } else {
        id_other.hide();
    }
}

function addMonth(dateText, months) {
    var d = $.datepicker.parseDate("dd/mm/yy", dateText);
    if (d.getMonth() == 1 && d.getDate() == 29 && months == 12)
    {
        d.setDate(d.getDate() - 1);
    }
    d.setMonth(d.getMonth() + months);

    return $.datepicker.formatDate('dd/mm/yy', d);
}

function deltaYear(dateText) {
    var sd = dateText.split("/");
    var  install_date = new Date(parseInt(sd[2]), parseInt(sd[1]), parseInt(sd[0]));
    var  now_date = new Date();
    return (now_date.getFullYear() - install_date.getFullYear());
}
"""

IMPIANTO_ADD_JS = __IMPIANTO_ADD_JS % (COMMON_FUNCTION)
VERIFICA_ADD_JS = __VERIFICA_ADD_JS % (COMMON_FUNCTION)
INTERVENTO_ADD_JS = __INTERVENTO_ADD_JS % (COMMON_FUNCTION)

