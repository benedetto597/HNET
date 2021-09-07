from odoo import models, fields


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    cuenta_id = fields.Many2one('account.analytic.account', string="Proyecto")

    def button_validate(self):
        res = super(StockPickingInherit, self).button_validate()
        asientos = self.env['account.move'].sudo().search([('ref', 'ilike', self.name)])

        if asientos and self.cuenta_id:
            for asiento in asientos:
                for line in asiento.line_ids:
                    line.analytic_account_id = self.cuenta_id.id

        return res
