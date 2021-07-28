from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    cai = fields.Char(string="CAI")
    rango = fields.Char(string="Rango Autorizado")
    rtn = fields.Char(string="RTN")
    razon = fields.Char(string="Razón Social")
    nombre = fields.Char(string="Nombre Comercial")
    correo = fields.Char(string="Correo")
    telefono = fields.Char(string="Teléfono")
    direccion = fields.Char(string="Dirección")
    rango_maximo = fields.Integer(string="Rango Máximo del CAI")
    fecha_expiracion = fields.Date(string="Fecha limite de Emisión")
