from odoo import models, fields


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    invoice_date = fields.Date(default=fields.Date.today())


class SaleSubscriptionInherit(models.Model):
    _inherit = "sale.subscription"

    def _prepare_invoice_data(self):
        res = super(SaleSubscriptionInherit, self)._prepare_invoice_data()
        res.pop("invoice_payment_term_id")
        res["invoice_date_due"] = False
        return res
