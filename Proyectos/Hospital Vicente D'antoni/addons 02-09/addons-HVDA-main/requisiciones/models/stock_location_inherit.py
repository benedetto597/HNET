from odoo import models, fields


class LocationInherit(models.Model):
    _inherit = "stock.location"

    cuenta_id = fields.Many2one('account.analytic.account', string="Cuenta")
