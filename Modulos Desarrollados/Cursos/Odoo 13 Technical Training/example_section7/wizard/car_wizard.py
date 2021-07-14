#-*- coding: utf-8 -*-

""" 
----------------------------------------------------------------------------------------------------
    @author edgar.benedetto@unah.hn 
    @date 14/07/2021
    @version 1.0
----------------------------------------------------------------------------------------------------
"""
# 41. Filters & Groups
from odoo import models, fields, api

class CarWizard(models.TransientModel):
    _name = "car.wizard"
    _description = "Cuadro de dialogo de carro"

    horse_power_plus = fields.Integer('Horse Power')

    # Acción del Wizard
    def add_horse_power(self):
        """ Imprimir el id del carro actual o activo """
        print('car_id',self.env.context.get('active_id'))
        print('horse_power',self.horse_power_plus)

        # Obtener el id del carro actual, y usar WRITE para reemplazar el valor actual por el escrito en el wizard
        self.env['car.car'].browse(self.env.context.get('active_id')).write({
            'horse_power':self.horse_power_plus
        })

        # Retornar el cierre del wizard
        return {'type':'ir.actions.act_window_close'}