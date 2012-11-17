#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERIFICA_ADD_JS = """
<script>
$(function() {
    if ($("#id_analisi_combustione").is(':checked')) {
    } else {
        $("#tr_colore_bollino").hide();
        $("#tr_numero_bollino").hide();
        $("#tr_valore_bollino").hide();
        $("#tr_scadenza_tra").hide();
    }

    $("#tr_altro_tipo_manutenzione").hide();
    $("#id_tipo_verifica option:selected").each(function () {
        if ($(this).text() == "Altro..") {
            $("#id_tipo_verifica").parent().append($("#id_altro_tipo_manutenzione"));
        } else {
            $("#id_altro_tipo_manutenzione").hide();
        }
    });


    $("#id_data_verifica").datepicker({
        showButtonPanel: true,
        dateFormat: "dd/mm/yy",
        currentText: "Oggi",
        closeText: "Chiudi",
        dayNames: [ "Domenica", "Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato" ],
        dayNamesShort: [ "Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab" ],
        monthNames: [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ],
        monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ]
    });


    $("#id_tipo_verifica").change(function () {
        var str = "";
        $("#id_tipo_verifica option:selected").each(function () {
            if ($(this).text() == "Altro..") {
                $("#id_tipo_verifica").parent().append($("#id_altro_tipo_manutenzione"));
                $("#id_altro_tipo_manutenzione").show("slow");
            } else {
                $("#id_altro_tipo_manutenzione").hide();
            }
        });
    });

    $("#id_analisi_combustione").click( function() {
        if ($(this).is(':checked')) {
            $("#tr_colore_bollino").show("slow");
            $("#tr_numero_bollino").show("slow");
            $("#tr_valore_bollino").show("slow");
        } else {
            $("#tr_valore_bollino").slideUp();
            $("#tr_numero_bollino").slideUp();
            $("#tr_colore_bollino").slideUp();
        }
    });
});
</script>
"""
