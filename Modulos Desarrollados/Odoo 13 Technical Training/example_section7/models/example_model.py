#-*- coding: utf-8 -*-

""" 
----------------------------------------------------------------------------------------------------
    @author edgar.benedetto@unah.hn 
    @date 12/07/2021
    @version 1.0
----------------------------------------------------------------------------------------------------
"""

from odoo import models, fields

class car(models.Model):
    """ Ejemplo seccion 7 """

    _name = 'car.car'

    name = fields.Char(string='Name')
    horse_power = fields.Integer(string='Horse Power')
    door_number = fields.Integer(string='Horse Number')
