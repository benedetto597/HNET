from odoo import models, fields, api


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    costo_directo = fields.Float("Costo Directo", digits="Product Price", compute="_get_costo_directo")

    @api.depends('purchase_price', 'product_uom_qty')
    def _get_costo_directo(self):
        for rec in self:
            rec.costo_directo = rec.purchase_price * rec.product_uom_qty
