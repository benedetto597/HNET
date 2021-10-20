# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Identificador de sesión de venta y orden de venta para picking (Herencia - Stock Picking)
    @name_file stock_picking_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api,fields, models

from itertools import groupby

class StockPicking(models.Model):
    _inherit='stock.picking'

    salesteam_session_id = fields.Many2one('salesteam.session')
    salesteam_order_id = fields.Many2one('sale.order')
