#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERIFICA_ADD_JS = """
<script>
$(function() {
    $("#td_colore_bollino").hide();
    $("#td_numero_bollino").hide();
    $("#td_valore_bollino").hide();
    $("#td_scadenza_tra").hide();
    $("#td_altro_tipo_manutenzione").hide();
    $("#id_data_verifica").datepicker();

    $("#id_altro_tipo_manutenzione").hide();
    $("#id_stato_pagamento").append("Si")

    $("#id_tipo_manutenzione").change(function () {
        var str = "";
        $("#id_tipo_manutenzione option:selected").each(function () {
            str += $(this).text();
        });
        if (str == "Altro..") {
            $("#id_tipo_manutenzione").parent().append($("#id_altro_tipo_manutenzione"));
            $("#id_altro_tipo_manutenzione").show("slow");
        } else {
            $("#id_altro_tipo_manutenzione").hide();
        }
    });

    $("#id_fumi_eseguiti").click( function() {
        if ($(this).is(':checked')) {
            $("#td_colore_bollino").show("slow");
            $("#td_numero_bollino").show("slow");
            $("#td_valore_bollino").show("slow");
        } else {
            $("#td_valore_bollino").slideUp();
            $("#td_numero_bollino").slideUp();
            $("#td_colore_bollino").slideUp();
        }
    });
});
</script>
"""
