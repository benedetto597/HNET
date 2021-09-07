from odoo import models, fields


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    invoice_date = fields.Date(default=fields.Date.today())

