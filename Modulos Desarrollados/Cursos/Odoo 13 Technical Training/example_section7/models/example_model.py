#-*- coding: utf-8 -*-

""" 
----------------------------------------------------------------------------------------------------
    @author edgar.benedetto@unah.hn 
    @date 12/07/2021
    @version 1.0
----------------------------------------------------------------------------------------------------
"""

from odoo import models, fields

class Car(models.Model):
    """ Ejemplo seccion 7 """

    _name = 'car.car'

    name = fields.Char(string='Name')
    door_number = fields.Integer(string='Horse Number')
    horse_power = fields.Integer(string='Horse Power')

    #13/07/2021
    # 26. Campo Many2one 
    # El primer parámetro es el modelo u objeto relacional Many
    driver_id = fields.Many2one('res.partner', string='Driver')
    parking_id = fields.Many2one('parking.parking', string="Parking")

    # 28. Campo Many2many
    feature_ids = fields.Many2many("car.feature", string="Features")

    # 29. Campo computado o calculado
    total_speed = fields.Integer(string="Speed Total", compute="get_total_speed")
    random_message = fields.Char(string="Message", compute="say_hello", readonly="True")


    def get_total_speed(self):
        """ 29. Campo calculado e impresiones en consola """
        # print('name', self.name)
        # print('horse_power', self.horse_power)
        self.total_speed = self.horse_power * 30

    def say_hello(self):
        """ 29. Campo calculado """
        # print('driver_id.', self.driver_id)
        # print('driver_id id.', self.driver_id.id)
        # print('driver_id name.', self.driver_id.name)
        self.random_message = ('hello {}'.format(self.driver_id.name))


class Parking(models.Model):
    """ Ejemplo seccion 8 Campo One2many """
    _name = "parking.parking"
    name = fields.Char(string="Name")

    """ El primer parámetro es el modelo Many (Muchos carros)
        El segundo parámetro es el modelo one (Tienen un solo parqueo)

        Todos los carros tendrán un solo parqueo
    """
    car_ids = fields.One2many('car.car', 'parking.parking', string="Cars")

class CarFeature(models.Model):
    """ Ejemplo sección 8 Campo Many2many"""
    _name = "car.feature"
    name = fields.Char(string="Name")

    