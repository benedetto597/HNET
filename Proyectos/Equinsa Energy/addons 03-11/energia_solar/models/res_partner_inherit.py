from odoo import models, fields, api


class ResPartnerTarifaInherit(models.Model):
    _inherit = 'res.partner'

    # Datos ingresados
    porcentaje_ahorro = fields.Float(string="Porcentaje de ahorro")
    codigo_cliente = fields.Char(string="Código de Cliente")
    region_cliente = fields.Selection([('eisps', 'EESPS'), ('eitgu', 'EETGU')], string="Región de Cliente")
    tipo_cliente = fields.Selection([
        ('normal', 'Tarifa USD'),
        ('otro', 'Tarifa HNL'),
        ('especial', 'Especial'),
        ('equinsa', 'EQUINSA')], string="Tipo de Cliente")
    tarifa_base1 = fields.Float(string="Tarifa Base1", help='Valor de la tarifa base en Dolares', digits=(12, 4))
    tarifa_base2 = fields.Float(string="Tarifa Base2", help='Piso Minimo', digits=(12, 4))
    tarifa_base3 = fields.Float(string="Tarifa Base3", help='Piso Maximo', digits=(12, 4))
