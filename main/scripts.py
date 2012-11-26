#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERIFICA_ADD_JS = """
<script>

$(function() {
    $("input[type=submit]").button()

    if (!$("#id_analisi_combustione").is(':checked')) {
        $("#tr_colore_bollino").hide();
        $("#tr_numero_bollino").hide();
        $("#tr_valore_bollino").hide();
        $("#tr_prossima_analisi_combustione").hide();
        $("#tr_scadenza_fumi_tra").hide();
    }

    $("#tr_altro_tipo_verifica").hide();
    $("#id_tipo_verifica option:selected").each(function () {
        if ($(this).text() == "Altro..") {
            $("#id_tipo_verifica").parent().append($("#id_altro_tipo_verifica"));
        } else {
            $("#id_altro_tipo_verifica").hide();
        }
    });

    $("#tr_altro_colore_bollino").hide();
    $("#id_colore_bollino option:selected").each(function () {
        if ($(this).text() == "Altro..") {
            $("#id_colore_bollino").parent().append($("#id_altro_colore_bollino"));
        } else {
            $("#id_altro_colore_bollino").hide();
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
        monthNamesShort: [ "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Aug", "Set", "Ott", "Nov", "Dic" ],
        onSelect: function(dateText) {
            $('#id_prossima_verifica').val( function() {
                var sd = dateText.split("/");
                var d = new Date(parseInt(sd[2]), parseInt(sd[1]), parseInt(sd[0]));
                d.setDate(d.getDate() + 365);
                return d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear();
            });
        }
    });

    $("#id_scadenza_verifica_tra").keyup(function () {
        var sd = $("#id_data_verifica").val().split("/");
        var d = new Date(parseInt(sd[2]), parseInt(sd[1]), parseInt(sd[0]));
        if ($(this).val()) {
            d.setMonth(d.getMonth() + parseInt($(this).val()));
            $('#id_prossima_verifica').val(d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear());
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
            } if else ($(this).text() == "Verde") {
                $("#id_scadenza_fumi_tra").val("12");
            } else {
                $("#id_altro_tipo_verifica").hide();
            }
        });
    });

    $("#id_colore_bollino").change(function () {
        var str = "";
        $("#id_colore_bollino option:selected").each(function () {
            if ($(this).text() == "Altro..") {
                $("#id_colore_bollino").parent().append($("#id_altro_colore_bollino"));
                $("#id_altro_colore_bollino").show("slow");
            } else {
                $("#id_altro_colore_bollino").hide();
            }
        });
    });


    $("#id_analisi_combustione").click( function() {
        if ($(this).is(':checked')) {
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
        var sd = $("#id_data_verifica").val().split("/");
        var d = new Date(parseInt(sd[2]), parseInt(sd[1]), parseInt(sd[0]));
        if ($(this).val()) {
            d.setMonth(d.getMonth() + parseInt($(this).val()));
            $('#id_prossima_analisi_combustione').val(d.getDate() + "/" + (parseInt(d.getMonth()) + 1) + "/" + d.getFullYear());
        } else {
            $('#id_prossima_analisi_combustione').val($('#id_data_verifica').val());
        }
    }).keyup();

});
</script>
"""


