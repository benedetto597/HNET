from odoo import models, api
from datetime import datetime


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, values):
        res = super(SaleOrderInherit, self).create(values)

        if values.get("x_negocio"):
            res_name = res.name.split('-')
            currentMonth = datetime.now().month
            valor = ("EE", res.x_negocio, res_name[0][-2:], '-', str(currentMonth), res_name[1])
            num_contrato = "".join(valor)
            res.x_contrato = num_contrato

        return res
