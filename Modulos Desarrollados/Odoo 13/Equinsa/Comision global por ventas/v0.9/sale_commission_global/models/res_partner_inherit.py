# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 03/11/2021
    @decription Identificar si un partner es Gerente
    @name_file res_partner_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""

from odoo import api, fields, models

class ResPartner(models.Model):
    """Add some fields related to commissions"""
    _inherit = "res.partner"

    manager = fields.Boolean(
        string="Gerencia",
        help="Define si el agente es el gerente para comisionar en todas las ventas",
        default=False    
    )