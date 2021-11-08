from odoo import models, fields, api


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'
    _description = 'Immediate Transfer'

    def process(self):
        res = super(StockImmediateTransfer, self).process()
        for pick in self.pick_ids:
            pick.update_product_cost()
        return res
