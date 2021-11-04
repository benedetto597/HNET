from odoo import models, fields, api


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta Analítica')

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        res = super(StockMoveInherit, self)._generate_valuation_lines_data(
            partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)

        if self.analytic_account_id and res['credit_line_vals']:
            res['credit_line_vals'].update({
                'analytic_account_id': self.analytic_account_id.id
            })

        if self.analytic_account_id and res['debit_line_vals']:
            res['debit_line_vals'].update({
                'analytic_account_id': self.analytic_account_id.id
            })
        return res

    def write(self, vals):
        res = super(StockMoveInherit, self).write(vals)
        if 'analytic_account_id' in vals and self.account_move_ids:
            ac_lines = self.account_move_ids.line_ids
            if ac_lines:
                for line in ac_lines:
                    aa_val = self.analytic_account_id.id if self.analytic_account_id else False
                    line.write({"analytic_account_id": aa_val})
        return res

