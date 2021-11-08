from odoo import models


class SaleOrderInherit(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()

        if self.analytic_account_id:
            move_ids = self.picking_ids.move_ids_without_package.mapped("id")
            moves = self.env['stock.move'].search([('id', 'in', move_ids)])

            for move in moves:
                move.analytic_account_id = self.analytic_account_id.id
        return res



