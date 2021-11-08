from odoo import models, fields, api


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    is_deposit = fields.Boolean("Es Depósito")

    def write(self, vals):
        if 'invoice_line_ids' in vals:
            sequence = 0
            for line in self.invoice_line_ids:
                sequence += 10
                line.sequence = sequence
        res = super(AccountMoveInherit, self).write(vals)
        return res

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        invoice = super(AccountMoveInherit, self).create(vals)
        sequence = 0
        for line in invoice.invoice_line_ids:
            sequence += 10
            line.sequence = sequence
        return invoice


class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInvInherit, self)._prepare_invoice_values(order, name, amount, so_line)
        res['is_deposit'] = True

        return res

