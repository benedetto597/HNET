from odoo import models, fields, api


class StockInventoryLineInherit(models.Model):
    _inherit = 'stock.inventory.line'

    marca = fields.Many2one('product.brand', string='Marca', compute="get_marca", store=True)

    @api.depends('product_id')
    def get_marca(self):
        for rec in self:
            prod = rec.product_id
            if prod and prod.product_tmpl_id and prod.product_tmpl_id.product_brand_id:
                rec.marca = prod.product_tmpl_id.product_brand_id.id
            else:
                rec.marca = False


class StockValuationLayerInherit(models.Model):
    _inherit = 'stock.valuation.layer'

    marca = fields.Many2one('product.brand', string='Marca', compute="get_marca", store=True)

    @api.depends('product_id')
    def get_marca(self):
        for rec in self:
            prod = rec.product_id
            if prod and prod.product_tmpl_id and prod.product_tmpl_id.product_brand_id:
                rec.marca = prod.product_tmpl_id.product_brand_id.id
            else:
                rec.marca = False


class StockQuantInherit(models.Model):
    _inherit = 'stock.quant'

    marca = fields.Many2one('product.brand', string='Marca', compute="get_marca", store=True)

    @api.depends('product_id')
    def get_marca(self):
        for rec in self:
            prod = rec.product_id
            if prod and prod.product_tmpl_id and prod.product_tmpl_id.product_brand_id:
                rec.marca = prod.product_tmpl_id.product_brand_id.id
            else:
                rec.marca = False


class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    marca = fields.Many2one('product.brand', string='Marca', compute="get_marca", store=True)

    @api.depends('product_id')
    def get_marca(self):
        for rec in self:
            prod = rec.product_id
            if prod and prod.product_tmpl_id and prod.product_tmpl_id.product_brand_id:
                rec.marca = prod.product_tmpl_id.product_brand_id.id
            else:
                rec.marca = False