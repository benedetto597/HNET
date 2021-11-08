from odoo import models, fields, api


class ResumenTransferencias(models.Model):
    _name = "resumen.transferencias"

    cantidad = fields.Float('Cantidad', digits='Product Unit of Measure')
    done = fields.Float('Cantidad Real', digits='Product Unit of Measure')
    product_id = fields.Many2one('product.product', 'Producto')
    project_id = fields.Many2one('project.project', 'Proyecto')
    costo = fields.Float(string='Costo Presupuestado', digits='Product Price')
    costo_real = fields.Float(string='Costo Real', digits='Product Price', store="True", compute="_get_costo_real")
    razon_desviacion_id = fields.Many2one('razon.desviacion', 'Razón de Desviación')

    valor_presupuestado = fields.Float(string="Valor Presupuestado", digits='Product Price', store="True", compute="_get_valor_presupuestado")
    valor_real = fields.Float(string="Valor Real", digits='Product Price', store="True", compute="_get_valor_real")
    desviacion_coste = fields.Float(string="Desviación Coste", digits='Product Price', store="True", compute="_get_desviacion_coste")
    desviacion_cantidad = fields.Float(string="Desviación Cantidad", digits='Product Price', store="True",
                                       compute="_get_desviacion_cantidad")
    desviacion_economica = fields.Float(string="Desviación Económica", digits='Product Price', store="True",
                                        compute="_get_desviacion_economica")

    @api.depends('cantidad', 'costo')
    def _get_valor_presupuestado(self):
        for rec in self:
            rec.valor_presupuestado = rec.cantidad * rec.costo

    @api.depends('product_id')
    def _get_costo_real(self):
        for rec in self:
            cost = 0
            if rec.product_id:
                cost = rec.product_id.standard_price
            rec.costo_real = cost

    @api.depends("done", "costo_real")
    def _get_valor_real(self):
        for rec in self:
            rec.valor_real = rec.done * rec.costo_real

    @api.depends('costo', 'costo_real')
    def _get_desviacion_coste(self):
        for rec in self:
            rec.desviacion_coste = rec.costo - rec.costo_real

    @api.depends('cantidad', 'done')
    def _get_desviacion_cantidad(self):
        for rec in self:
            rec.desviacion_cantidad = rec.cantidad - rec.done

    @api.depends('valor_real', 'valor_presupuestado')
    def _get_desviacion_economica(self):
        for rec in self:
            rec.desviacion_economica = rec.valor_presupuestado - rec.valor_real
