from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    costos_directos = fields.Float("Costos Directos", digits="Product Price", compute="_get_costos_directos")
    costo_indirecto = fields.Float("Costos Directos", digits="Product Price", compute="_get_costo_indirecto")
    imprevistos = fields.Float("Imprevistos", digits="Product Price", compute="_get_imprevistos")
    gastos_admin = fields.Float("Gastos Administrativos", digits="Product Price", compute="_get_gastos_admin")
    utilidad = fields.Float("Utilidad", digits="Product Price", compute="_get_utilidad")
    precio_venta = fields.Float("Precio de Venta", digits="Product Price", compute="_get_precio_venta")

    @api.depends('order_line')
    def _get_costos_directos(self):
        for rec in self:
            rec.costos_directos = sum(rec.order_line.mapped('costo_directo'))

    @api.depends('imprevistos', 'gastos_admin', 'commission_total', 'utilidad')
    def _get_costo_indirecto(self):
        for rec in self:
            rec.costos_indirectos = rec.imprevistos + rec.gastos_admin + rec.commission_total + rec.utilidad

    @api.depends('costos_directos')
    def _get_imprevistos(self):
        for rec in self:
            rec.imprevistos = rec.costos_directos * 0.1

    @api.depends('costos_directos')
    def _get_gastos_admin(self):
        for rec in self:
            rec.gastos_admin = rec.costos_directos * 0.1

    @api.depends('costos_directos', 'costo_indirecto')
    def _get_utilidad(self):
        for rec in self:
            rec.utilidad = rec.costos_directos - (rec.imprevistos + rec.gastos_admin + rec.commission_total)

    @api.depends('costos_directos', 'costo_indirecto')
    def _get_precio_venta(self):
        for rec in self:
            rec.precio_venta = rec.costos_directos + rec.costo_indirecto



