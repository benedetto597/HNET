# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/10/2021
    @decription Agregar a la plantilla de cirugia el campo Total del precio de consumibles
    @name_file surgery_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models, _

class ACSSurgeryInherit(models.Model):
    _inherit = "hms.surgery.template"
    _description = "Surgery total consumibles"

    total_consumables = fields.Float(string='Total', help='Total de los productos a consumir', compute='_compute_total',)

    @api.depends('consumable_line_ids')
    def _compute_total(self):
        """ Calcular el total de los consumibles sumando los subtotales """
        total_price = 0
        for rec in self:
            for consumible in rec.consumable_line_ids: total_price += consumible.product_subtotal

        self.total_consumables = total_price