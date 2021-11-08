from odoo import models, fields, api
from ast import literal_eval


class ProjectProjectInherit(models.Model):
    _inherit = "project.project"

    resumen_ids = fields.One2many('resumen.transferencias', 'project_id', copy=False)
    total_presupuestado = fields.Float('Total Presupuestado', compute='_get_total_presupuestado', copy=False)
    total_real = fields.Float('Total Real', compute='_get_total_real', copy=False)
    total_desviacion_costo = fields.Float('Total Desviación Costo', compute='_get_total_desviacion_costo', copy=False)
    total_desviacion_cantidad = fields.Float('Total Desviación cantidad', compute='_get_total_desviacion_cantidad', copy=False)
    total_desviacion_economica = fields.Float('Total Desviación Económica', compute='_get_total_desviacion_economica', copy=False)
    total_utilidad = fields.Float('Total Utilidad', compute='_get_total_utilidad', copy=False)
    total_imprevistos = fields.Float('Total Imprevistos', compute='_get_total_imprevistos', copy=False)
    total_administracion = fields.Float('Total Administración', compute='_get_total_administracion', copy=False)

    def _get_sales(self):
        orders = False
        if self.analytic_account_id:
            orders = self.env['sale.order'].search([('analytic_account_id', '=', self.analytic_account_id.id)])
        return orders

    # INFORME
    @api.depends('resumen_ids')
    def _get_total_presupuestado(self):
        for rec in self:
            val = 0
            if rec.resumen_ids:
                val = sum(rec.resumen_ids.mapped('costo'))
            rec.total_presupuestado = val

    @api.depends('resumen_ids')
    def _get_total_real(self):
        for rec in self:
            val = 0
            if rec.resumen_ids:
                val = sum(rec.resumen_ids.mapped('costo_real'))
            rec.total_real = val

    @api.depends('resumen_ids')
    def _get_total_desviacion_costo(self):
        for rec in self:
            val = 0
            if rec.resumen_ids:
                val = sum(rec.resumen_ids.mapped('desviacion_coste'))
            rec.total_desviacion_costo = val

    @api.depends('resumen_ids')
    def _get_total_desviacion_cantidad(self):
        for rec in self:
            val = 0
            if rec.resumen_ids:
                val = sum(rec.resumen_ids.mapped('desviacion_cantidad'))
            rec.total_desviacion_cantidad = val

    @api.depends('resumen_ids')
    def _get_total_desviacion_economica(self):
        for rec in self:
            val = 0
            if rec.resumen_ids:
                val = sum(rec.resumen_ids.mapped('desviacion_economica'))
            rec.total_desviacion_economica = val

    # COTIZACIÓN

    @api.depends('analytic_account_id')
    def _get_total_utilidad(self):
        for rec in self:
            val = 0
            orders = self._get_sales()
            if orders:
                val = sum(orders.mapped('util_sum'))
            rec.total_utilidad = val

    @api.depends('analytic_account_id')
    def _get_total_imprevistos(self):
        for rec in self:
            val = 0
            orders = self._get_sales()
            if orders:
                val = sum(orders.mapped('imp_sum'))
            rec.total_imprevistos = val

    @api.depends('analytic_account_id')
    def _get_total_administracion(self):
        for rec in self:
            val = 0
            orders = self._get_sales()
            if orders:
                val = sum(orders.mapped('admin_sum'))
            rec.total_administracion = val

    def open_stock_moves(self):
        orders = self.env['sale.order'].search([('analytic_account_id', '=', self.analytic_account_id.id)])
        pickings = orders.picking_ids.move_ids_without_package
        dic = self.get_new_pick_lines(pickings)

        for item in dic:
            existe = False
            for line in self.resumen_ids:
                if item == line.product_id.id:
                    existe = True
                    line.cantidad = dic[item]['cantidad'] + line.cantidad
                    line.done = dic[item]['done'] + line.done
                    break
            if not existe:
                self.env['resumen.transferencias'].create(dic[item])

        moves = self.resumen_ids
        domain = [('id', 'in', moves.mapped("id"))]
        action = self.env.ref('resumen_pres_ent.resumen_action').read()[0]
        context = literal_eval(action['context'])
        context.update(self.env.context)
        res = dict(action, domain=domain, context=context)
        return res

    def update_dic(self, line, dic):
        sale_line = line.sale_line_id
        dic.update({
            # 'cantidad': dic['cantidad'] + (sale_line.product_uom_qty if sale_line else line.product_uom_qty),
            'done': dic['done'] + line.quantity_done,
        })
        return dic

    def create_dic(self, line, dic):
        sale_line = line.sale_line_id
        prod = line.product_id

        dic[prod.id] = {
            'costo': sale_line.purchase_price if sale_line else 0,
            'cantidad': sale_line.product_uom_qty if sale_line else 0,
            'done': line.quantity_done,
            'project_id': self.id,
            'product_id': prod.id,
        }

        return dic

    def get_new_pick_lines(self, pickings):
        dic = {}
        for line in pickings:
            # line.counted = False
            if not line.counted:
                if line.product_id.id not in dic:
                    dic.update(self.create_dic(line, dic))
                else:
                    dic[line.product_id.id] = self.update_dic(line, dic[line.product_id.id])
                line.counted = True
        return dic
