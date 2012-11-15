#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERIFICA_ADD_JS = """
<script>
$(function() {
    $("#td_colore_bollino").hide()
    $("#td_numero_bollino").hide()
    $("#td_valore_bollino").hide()

    $("#id_fumi").click( function() {
        if ($(this).is(':checked')) {
            $("#td_colore_bollino").show("slow")
            $("#td_numero_bollino").show("slow")
            $("#td_valore_bollino").show("slow")
        } else {
            $("#td_valore_bollino").slideUp()
            $("#td_numero_bollino").slideUp()
            $("#td_colore_bollino").slideUp()
        }
    });
});
</script>
"""
