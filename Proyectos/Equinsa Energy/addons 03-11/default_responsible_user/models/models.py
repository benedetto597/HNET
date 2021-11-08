from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    @api.model_create_multi
    def create(self, vals_list):
        res = super(StockPickingInherit, self).create(vals_list)
        if not res.user_id:
            res.user_id = res.create_uid.id
        return res

