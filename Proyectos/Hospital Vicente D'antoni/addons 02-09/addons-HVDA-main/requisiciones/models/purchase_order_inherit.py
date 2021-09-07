from odoo import models, fields, api, _


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    requisicion_con_id = fields.Many2one("requisiciones.condensadas", "Documento de Requisicion")


