from odoo import models, fields, api, _


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    def _prepare_invoice(self):

        invoice_vals = super(PurchaseOrderInherit, self)._prepare_invoice()
        invoice_vals['po_id'] = self.id

        return invoice_vals
