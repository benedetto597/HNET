from odoo import models, fields, api, _


class AccountTaxInherit(models.Model):
    _inherit = "account.tax"

    requisicion_lin_id = fields.Many2one("requisicion.lineas", "Linea de Requesicion")