from odoo import models, fields


class RazonDesviacion(models.Model):
    _name = "razon.desviacion"

    name = fields.Char("Nombre", required=True)
    description = fields.Char("Descripción")
