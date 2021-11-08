from odoo import models, fields, api


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    coste = fields.Float(string='Costo', digits='Product Price', default=0)
    coste_ent = fields.Float(string="Coste entregado", digits='Product Price', compute="_get_coste_ent")
    coste_pre = fields.Float(string="Coste Presupuestado", digits='Product Price', compute="_get_coste_pre")
    coste_total = fields.Float(string="Coste Total", digits='Product Price', compute="_get_coste_total")

    @api.depends('product_uom_qty', 'coste')
    def _get_coste_pre(self):
        for rec in self:
            rec.coste_pre = rec.product_uom_qty * rec.coste

    @api.depends('quantity_done', 'coste')
    def _get_coste_ent(self):
        for rec in self:
            rec.coste_ent = rec.quantity_done * rec.coste

    @api.depends('coste_ent', 'coste_pre')
    def _get_coste_total(self):
        for rec in self:
            rec.coste_total = rec.coste_pre - rec.coste_ent

    def product_id_coste_cambio(self):
        if not self.coste:
            self.coste = self.product_id.standard_price
