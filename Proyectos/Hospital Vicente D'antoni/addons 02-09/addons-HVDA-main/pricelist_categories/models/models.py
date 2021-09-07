from odoo import models, fields, api


class pricelist_categories(models.Model):
    _inherit = 'product.pricelist'

    pricelist_item_id = fields.Many2one('product.pricelist.item', 'Ejemplo Lista de precio', ondelete='cascade')
    cat_name = fields.Char('Identificador Categoria')

    def pricelist_item_vals(self, cat):
        pli = self.pricelist_item_id
        vals = {
        "applied_on": pli.applied_on,
        "categ_id": cat.id if cat else False,
        "product_tmpl_id": pli.product_tmpl_id.id if pli.product_tmpl_id else False,
        "product_id": pli.product_id.id if pli.product_id else False,
        "min_quantity": pli.min_quantity,
        "base": pli.base,
        "pricelist_id": pli.pricelist_id.id if pli.pricelist_id else False,
        "base_pricelist_id": pli.base_pricelist_id.id if pli.base_pricelist_id else False,
        "price_surcharge": pli.price_surcharge,
        "price_discount": pli.price_discount,
        "price_round": pli.price_round,
        "price_min_margin": pli.price_min_margin,
        "price_max_margin": pli.price_max_margin,
        "date_start": pli.date_start,
        "date_end": pli.date_end,
        "compute_price": pli.compute_price,
        "fixed_price": pli.fixed_price,
        "percent_price": pli.percent_price,
        }
        rec = self.env["product.pricelist.item"].create(vals)
        return rec

    def action_duplicate_item(self):
        if self.pricelist_item_id and self.pricelist_item_id.categ_id:
            categ_ids = self.env["product.category"].search([]).filtered(lambda cat: self.cat_name in cat.complete_name)
            if categ_ids:
                for cat in categ_ids:
                    if cat.id == self.pricelist_item_id.categ_id.id: continue
                    self.pricelist_item_vals(cat)
                    
