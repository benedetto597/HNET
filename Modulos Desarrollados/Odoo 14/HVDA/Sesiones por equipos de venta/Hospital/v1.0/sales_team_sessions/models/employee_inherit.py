# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Agregar el campo del equipo de venta al empleado (Herencia - HR Employee)
    @name_file employee_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import fields, models

class Employee(models.Model):
    _inherit = 'hr.employee'

    crm_team_id = fields.Many2one('crm.team', related='user_id.sale_team_id', string="Equipo de ventas", readonly=True)
