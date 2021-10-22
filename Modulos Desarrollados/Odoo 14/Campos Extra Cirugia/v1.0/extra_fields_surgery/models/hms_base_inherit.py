# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/10/2021
    @decription Agregar los campos calculados Precio Unitario y Subtotal a la linea de consumibles
    @name_file hms_base_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models, _

class ACSAppointmentConsumableInherit(models.Model):
    _inherit = "hms.consumable.line"

    product_unit_price = fields.Float(string='Precio por unidad', help='Precio del producto por unidad', compute='_compute_unit_price',required = True, default=1.0)
    product_subtotal = fields.Float(string='Subtotal', help='Subtotal (Cantidad x Precio Unitario', compute='_compute_subtotal')

    @api.depends('product_id')
    def _compute_unit_price(self):
        """ Extraer el precio por unidad del producto en la linea de consumibles """
        index = 0
        for rec in self:
            rec.product_unit_price = ((self.product_id)[index]).list_price
            index += 1 

    @api.depends('product_id', 'qty')
    def _compute_subtotal(self):
        """ Calcular subtotal (Precio Unidad * Cantidad) de los productos en la linea de consumibles """
        for rec in self: rec.product_subtotal = rec.qty * rec.product_unit_price 
