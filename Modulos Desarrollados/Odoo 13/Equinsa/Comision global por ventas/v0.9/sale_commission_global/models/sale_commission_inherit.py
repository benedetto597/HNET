# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 03/11/2021
    @decription Identificar si una comisión es Gerente
    @name_file sale_commission_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import _, api, exceptions, fields, models


class SaleCommission(models.Model):
    _inherit = "sale.commission"

    manager = fields.Boolean(
        string="Comisión Gerencia",
        help="Define si el agente es el gerente para comisionar en todas las ventas",
        default=False    
    )