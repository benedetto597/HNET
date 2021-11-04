from odoo import models, fields, api


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    costo_directo = fields.Float("Costo Directo", digits="Product Price", compute="_get_costo_directo")
    administracion = fields.Float(string="porcentaje Administración", compute="_get_administracion")
    imprevistos = fields.Float(string="porcentaje Imprevistos", compute="_get_imprevistos")
    utilidad = fields.Float(string="porcentaje Utilidad", compute="_get_utilidad")
    incentivos = fields.Float(string="porcentaje Incentivos", compute="_get_incentivos")
    util = fields.Float(string="util. %", related="util_temp", store=True, readonly=False)
    util_temp = fields.Float(string="util. % temp", compute="_get_util")

    # Campos calculados
    g = fields.Float("G", digits="Product Price", compute="_get_g")
    g_percent = fields.Float("G %", digits="Product Price", compute="_get_g_percent")
    j = fields.Float("J", digits="Product Price", compute="_get_j")
    j_percent = fields.Float("J %", digits="Product Price", compute="_get_j_percent")
    m = fields.Float("M", digits="Product Price", compute="_get_m")
    m_percent = fields.Float("M %", digits="Product Price", compute="_get_m_percent")
    s = fields.Float("S", digits="Product Price", compute="_get_s")
    s_percent = fields.Float("S %", digits="Product Price", compute="_get_s_percent")
    pv_temp = fields.Float("PV Temp", digits="Product Price", compute="_get_pv_temp")
    margen_utilidad = fields.Float("Margen de utilidad", compute="_get_margen_uti")

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLineInherit, self).product_uom_change()

        if self.pv_temp != 0 and self.order_id.x_negocio != "RT":
            self.price_unit = self.pv_temp
        return res

    @api.depends('purchase_price', 'pv_temp')
    def _get_margen_uti(self):
        for rec in self:
            if rec.pv_temp != 0 and rec.order_id.x_negocio != "RT":
                rec.margen_utilidad = (rec.pv_temp - rec.purchase_price)
            else:
                rec.margen_utilidad = (rec.price_unit - rec.purchase_price)

    @api.depends("purchase_price", "margen_utilidad")
    def _get_util(self):
        for rec in self:
            val = 0
            if rec.purchase_price > 0:
                val = (rec.margen_utilidad / rec.purchase_price) * 100
            rec.util_temp = val

    @api.onchange('util')
    def util_cambio(self):
        if self.product_id and self.purchase_price > 0:
            self.price_unit = ((self.util / 100) * self.purchase_price) + self.purchase_price

    @api.onchange('product_id')
    def product_id_change(self):
        precio = self.price_unit
        res =super(SaleOrderLineInherit, self).product_id_change()
        if self.order_id.state in ['sale', 'done', 'cancel']:
            self.price_unit = precio
            return res
        if self.pv_temp != 0 and self.order_id.x_negocio != "RT":
            self.price_unit = self.pv_temp
        return res

    def create(self, vals_list):
        res = super(SaleOrderLineInherit, self).create(vals_list)
        for rec in res:
            if rec.pv_temp != 0 and rec.order_id.x_negocio != "RT":
                rec.price_unit = rec.pv_temp
        return res

    @api.depends('purchase_price', 'product_uom_qty')
    def _get_costo_directo(self):
        for rec in self:
            rec.costo_directo = rec.purchase_price * rec.product_uom_qty

    # obtener porcentajes administrativos
    def _get_administracion(self):
        for rec in self:
            rec.administracion = self.env['ir.config_parameter'].get_param('cc_cotizaciones.administracion') or 0

    def _get_imprevistos(self):
        for rec in self:
            rec.imprevistos = self.env['ir.config_parameter'].get_param('cc_cotizaciones.imprevistos') or 0

    def _get_utilidad(self):
        for rec in self:
            rec.utilidad = self.env['ir.config_parameter'].get_param('cc_cotizaciones.utilidad') or 0

    def _get_incentivos(self):
        for rec in self:
            rec.incentivos = self.env['ir.config_parameter'].get_param('cc_cotizaciones.incentivos') or 0

    # obtener campos calculados
    @api.depends('administracion', 'costo_directo')
    def _get_g(self):
        for rec in self:
            rec.g = rec.administracion * rec.costo_directo

    @api.depends('costo_directo', 'g')
    def _get_g_percent(self):
        for rec in self:
            percent = 0
            if rec.costo_directo != 0:
                percent = (rec.g / rec.costo_directo)*100
            rec.g_percent = percent

    @api.depends('imprevistos', 'costo_directo')
    def _get_j(self):
        for rec in self:
            rec.j = rec.imprevistos * rec.costo_directo

    @api.depends('costo_directo', 'j')
    def _get_j_percent(self):
        for rec in self:
            percent = 0
            if rec.costo_directo != 0:
                percent = (rec.j / rec.costo_directo)*100
            rec.j_percent = percent


    @api.depends('utilidad', 'costo_directo')
    def _get_m(self):
        for rec in self:
            res_m = 0
            if rec.utilidad != 0:
                res_m = (rec.costo_directo / rec.utilidad) - rec.costo_directo
            rec.m = res_m

    @api.depends('utilidad')
    def _get_m_percent(self):
        for rec in self:
            rec.m_percent = (1 - rec.utilidad) *100

    @api.depends('incentivos', 'm')
    def _get_s(self):
        for rec in self:
            rec.s = rec.incentivos * rec.m

    @api.depends('s', 'm')
    def _get_s_percent(self):
        for rec in self:
            percent = 0
            if rec.m != 0:
                percent = (rec.s / rec.m) * 100
            rec.s_percent = percent

    @api.depends('product_uom_qty', 'costo_directo', 'g', 'j', 's', 'm')
    def _get_pv_temp(self):
        for rec in self:
            res = 0
            if rec.product_uom_qty > 0:
                suma = rec.costo_directo + rec.g + rec.j + rec.s + rec.m
                res = suma / rec.product_uom_qty
            rec.pv_temp = res

