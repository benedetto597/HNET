from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(StockPickingInherit, self).button_validate()
        self.update_product_cost()
        return res

    def update_product_cost(self):
        for mov in self.move_ids_without_package:
            if mov.coste == 0:
                mov.coste = mov.product_id.standard_price

