from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    margen_porcentaje = fields.Float("Margen %", compute="_calculo_porcentaje")

    @api.depends('amount_untaxed', 'margin')
    def _calculo_porcentaje(self):
        for rec in self:
            margin = 0
            if rec.amount_untaxed != 0 and rec.margin != 0:
                margin = (rec.margin / rec.amount_untaxed) * 100

            rec.margen_porcentaje = margin



