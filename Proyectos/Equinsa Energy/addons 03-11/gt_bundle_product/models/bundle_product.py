# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class productProduct(models.Model):
    
    _inherit = 'product.product'
    
    bundle_product = fields.Boolean(string="Is Bundle Product ?")
    bundle_product_ids = fields.One2many('bundle.product','prod_id',string="Bundle Products") 


class stockMove(models.Model):  
      
    _inherit = 'stock.move'
    
    # @api.model
    # def create(self, vals):
    #     _logger.info("stockmove=================== %s", vals)
    #     res = super(stockMove, self).create(vals)
    #     data = False
    #     if vals.get('product_id'):
    #         pobj = self.env['product.product'].browse(vals.get('product_id'))
    #         if pobj.bundle_product:
    #             for each in pobj.bundle_product_ids:
    #                 _logger.info("each=================== %s", each.name.id)
    #                 data = res.copy({
    #                     'product_id': each.name.id,
    #                     'product_uom_qty': each.quantity * res.product_uom_qty,
    #                     'product_uom': each.name.uom_id.id
    #                 })
    #             # res.unlink()
    #             _logger.info("data=================== %s", data)
    #             return data
    #     return res

    @api.model
    def create(self, vals):
        res = super(stockMove, self).create(vals)

        data = []
        if vals.get('product_id') and vals.get('sale_line_id'):
            pobj = self.env['product.product'].browse(vals.get('product_id'))
            if pobj.bundle_product:
                for each in pobj.bundle_product_ids:
                    data.append(res.copy({
                        'product_id': each.name.id,
                        'product_uom_qty': each.quantity * res.product_uom_qty,
                        'product_uom': each.unit_id.id
                    }).id)
                return self.browse(data)
        return res


class bundleProduct(models.Model):
    _name = "bundle.product"
    
    name = fields.Many2one('product.product', string="Nombre")
    quantity = fields.Float(string="Cantidad", digits='Product Unit of Measure')
    prod_id = fields.Many2one('product.product', string="Producto")
    unit_id = fields.Many2one('uom.uom', 'Unidad de Medida')

    @api.model
    def create(self,vals):
        if vals.get('name'):
            prod_obj = self.env['product.product'].browse(vals.get('name'))
            vals.update({'unit_id':prod_obj.uom_id.id})
        return super(bundleProduct, self).create(vals)
