from odoo import models


class SaleOrderInherit(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        if self.order_line and self.picking_ids:
            for line in self.order_line:
                prod = line.product_id
                op = self.picking_ids.move_ids_without_package.filtered(lambda o: o.product_id.id == prod.id)
                if op:
                    op.write({"coste": line.purchase_price})

        return res



