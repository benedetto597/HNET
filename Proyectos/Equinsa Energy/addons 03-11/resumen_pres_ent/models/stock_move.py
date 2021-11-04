from odoo import models, fields


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    counted = fields.Boolean('is counted')
