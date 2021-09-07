from odoo import models, fields, api, _


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    gasto_chk = fields.Boolean('Gasto')
