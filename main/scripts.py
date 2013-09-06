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


__IMPIANTO_JS = """
<script>
%s

$("[id=row_altra_potenza_caldaia]").hide()
if($("#id_potenza_caldaia").val() == "altro") {
    $("[id=row_altra_potenza_caldaia]").show();
}

$("[id=row_altro_tipo_caldaia]").hide();
if($("#id_tipo_caldaia").val() == "altro") {
    $("[id=row_altro_tipo_caldaia]").show();
}

$("#id_potenza_caldaia").change(function () {
    $("[id=row_altra_potenza_caldaia]").show("slow");
    if($("#id_potenza_caldaia").val() != "altro") {
        $("[id=row_altra_potenza_caldaia]").hide();
    }
});

$("#id_tipo_caldaia").change(function () {
    $("[id=row_altro_tipo_caldaia]").show("slow");
    if($("#id_tipo_caldaia").val() != "altro") {
        $("[id=row_altro_tipo_caldaia]").hide();
    }
});

$('#id_data_installazione').datepicker();
$('#id_data_contratto').datepicker();

</script>
"""

__VERIFICA_JS = """
<script>
%s

function show_provaFumi() {
    $("[id=row_colore_bollino]").show("slow");
    $("[id=row_numero_bollino]").show("slow");
    $("[id=row_valore_bollino]").show("slow");
    $("[id=row_prossima_analisi_combustione]").show("slow");
    $("[id=row_scadenza_fumi_tra]").show("slow");
}

function hide_provaFumi() {
    $("[id=row_colore_bollino]").hide();
    $("[id=row_numero_bollino]").hide();
    $("[id=row_valore_bollino]").hide();
    $("[id=row_prossima_analisi_combustione]").hide();
    $("[id=row_scadenza_fumi_tra]").hide();
    $("[id=row_altro_colore_bollino]").hide();
}

if($("#id_tipo_verifica").val() != "provafumi" || $("#id_tipo_verifica").val() != "prima_accensione") {
    hide_provaFumi();
}

$("[id=row_altro_colore_bollino]").show("slow");
if($("#id_colore_bollino").val() != "altro") {
    $("[id=row_altro_colore_bollino]").hide();
}

$("[id=row_analisi_combustione]").hide();

if($("#id_tipo_verifica").val() == "altro") {
    $("[id=row_altro_tipo_verifica]").show("slow");
} else {
    $("[id=row_altro_tipo_verifica]").hide();
}

$("#id_tipo_verifica").change(function () {
    $("#id_tipo_verifica option:selected").each(function () {
        if ($(this).val() == "altro") {
            $("[id=row_altro_tipo_verifica]").show("slow");
        } else {
            $("[id=row_altro_tipo_verifica]").hide();
        }
    });
});

$("#id_tipo_verifica").change( function() {
    if ($(this).val() == "provafumi" || $(this).val() == "prima_accensione") {
        show_provaFumi();
    } else {
        hide_provaFumi();
    }
});

$("#id_data_verifica").datepicker().on('changeDate', function(ev) {
    $('#id_prossima_verifica').val(addMonth($(this).val(), 12));
});

$('#id_prossima_verifica').datepicker();
$('#id_prossima_analisi_combustione').datepicker();

$("#id_scadenza_verifica_tra").keyup(function () {
    this.value = this.value.replace(/[^0-9\.]/g,'');
    if ($(this).val()) {
        $('#id_prossima_verifica').val(addMonth($("#id_data_verifica").val(), parseInt($(this).val())));
    } else {
        $('#id_prossima_verifica').val($('#id_data_verifica').val());
    }
}).keyup();

$("#id_scadenza_fumi_tra").keyup(function () {
    this.value = this.value.replace(/[^0-9\.]/g,'');
    if ($(this).val()) {
        $('#id_prossima_analisi_combustione').val(addMonth($("#id_data_verifica").val(), parseInt($(this).val())));
    } else {
        $('#id_prossima_analisi_combustione').val($('#id_data_verifica').val());
    }
}).keyup();

var potenza_caldaia = $("#row_potenza_caldaia").text();
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

$("#id_colore_bollino").change(function () {
    var scadenza_mesi = 24;
    var colore_bollino_sel = $("#id_colore_bollino option:selected").val()
    if (colore_bollino_sel  == "altro") {
        $("[id=row_altro_colore_bollino]").show("slow");
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
        $("[id=row_altro_colore_bollino]").hide();
    }
    $("#id_scadenza_fumi_tra").val(scadenza_mesi);
    $('#id_prossima_analisi_combustione').val(addMonth($("#id_data_verifica").val(), scadenza_mesi));
});

</script>
"""

__INTERVENTO_JS = """
<script>
%s
$('#id_data_intervento').datepicker();
</script>
"""

COMMON_FUNCTION = """

function addMonth(date_text, months) {
    var d = $.datepicker.parseDate("dd/mm/yy", date_text);
    if (d.getMonth() == 1 && d.getDate() == 29 && months == 12)
    {
        d.setDate(d.getDate() - 1);
    }
    d.setMonth(d.getMonth() + months);
    return $.datepicker.formatDate("dd/mm/yy", d);
}

function deltaYear(dateText) {
    var sd = dateText.split("/");
    var  install_date = new Date(parseInt(sd[2]), parseInt(sd[1]), parseInt(sd[0]));
    var  now_date = new Date();
    return (now_date.getFullYear() - install_date.getFullYear());
}
"""

IMPIANTO_JS = __IMPIANTO_JS % (COMMON_FUNCTION)
VERIFICA_JS = __VERIFICA_JS % (COMMON_FUNCTION)
INTERVENTO_JS = __INTERVENTO_JS % (COMMON_FUNCTION)

