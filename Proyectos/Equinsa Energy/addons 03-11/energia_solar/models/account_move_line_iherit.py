from odoo import models


class AccountMoveLineDataInherit(models.Model):
    _inherit = 'account.move.line'

    def write(self, vals):
        if self.subscription_id:
            self = self.with_context(check_move_validity=False)
        res = super(AccountMoveLineDataInherit, self).write(vals)

        return res
