from odoo import fields, models


class res_currency(models.Model):
    _inherit = "res.currency"

    currency_name = fields.Char('Currency Name', help="Currency Full name as known in the world")
