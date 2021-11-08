from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    admin_sum = fields.Float("Administración", digits="Product Price", compute="_get_admin_sum")
    imp_sum = fields.Float("Imprevistos", digits="Product Price", compute="_get_imp_sum")
    util_sum = fields.Float("Utilidad", digits="Product Price", compute="_get_util_sum")
    util_sum_percent = fields.Float("Utilidad %", digits="Product Price", compute="_get_util_sum_percent")
    incen_sum = fields.Float("Incentivos", digits="Product Price", compute="_get_incen_sum")

    @api.depends('order_line')
    def _get_admin_sum(self):
        for rec in self:
            rec.admin_sum = sum(rec.order_line.mapped('g'))

    @api.depends('order_line')
    def _get_imp_sum(self):
        for rec in self:
            rec.imp_sum = sum(rec.order_line.mapped('j'))

    @api.depends('order_line')
    def _get_util_sum(self):
        for rec in self:
            rec.util_sum = sum(rec.order_line.mapped('m'))

    @api.depends('util_sum', 'amount_untaxed')
    def _get_util_sum_percent(self):
        for rec in self:
            percent = 0
            if rec.amount_untaxed != 0 and rec.util_sum != 0:
                percent = (rec.util_sum / rec.amount_untaxed) * 100
            rec.util_sum_percent = percent

    @api.depends('order_line')
    def _get_incen_sum(self):
        for rec in self:
            rec.incen_sum = sum(rec.order_line.mapped('s'))
