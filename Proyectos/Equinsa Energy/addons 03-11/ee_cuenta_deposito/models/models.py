from odoo import models, fields, api


class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInvInherit, self)._prepare_invoice_values(order, name, amount, so_line)

        if 'invoice_line_ids' in res:
            for j, k, l in res['invoice_line_ids']:
                l['account_id'] = self.deposit_account_id.id,
        return res
