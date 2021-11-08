# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 24/10/2021
    @decription Agregar el campo que determinará cuando una orden está cerrada
    @name_file sale_order_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models, _

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    order_close = fields.Boolean(
        string="Orden Cerrada?",
        help="Si al paciente se le dio de alta la orden se declara cerrada",
        default = False)

    can_edit = fields.Selection([('yes','Yes'),('no','No')], string='Can Edit', compute='_compute_can_edit')

    def close_order(self):
        self.order_close = True

    @api.depends('order_close')
    def _compute_can_edit(self):
        if self.order_close == False:
            self.can_edit = 'yes'
        else:
            self.can_edit = 'no'