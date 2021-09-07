from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RequisicionesCondensadas(models.Model):
    _name = 'requisiciones.condensadas'
    _description = 'requisiciones.condensadas'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), track_visibility='onchange')
    compras_count = fields.Integer(string='Compras', compute='_get_compras', readonly=True)
    requesicion_line_ids = fields.One2many(comodel_name="requisicion.lineas", inverse_name="requisicion_con_id")
    total = fields.Monetary(string='Total', compute="_get_total")
    purchase_ids = fields.One2many('purchase.order', 'requisicion_con_id', string='Ordenes de Compra')
    note = fields.Text('Notas')
    currency_id = fields.Many2one('res.currency', string="Moneda",
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.user.company_id,
        required=True,
        copy=True,
    )

    # CREATE WRITE AND UNLINK FUNCTION
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('requisicion.con.sequence') or _('New')
        result = super(RequisicionesCondensadas, self).create(vals)
        return result

    @api.depends('purchase_ids')
    def _get_compras(self):
        for rec in self:
            rec.compras_count = len(rec.purchase_ids)

    @api.depends('requesicion_line_ids')
    def _get_total(self):
        for rec in self:
            total = sum(rec.requesicion_line_ids.mapped('total'))
            rec.total = total

    def action_view_purchase_orders(self):
        purchases = self.mapped('purchase_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_form_action")
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]
        elif len(purchases) == 1:
            form_view = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = purchases.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'gasto',
        }
        action['context'] = context
        return action

    def create_POL(self, po):
        pol_env = self.env['purchase.order.line']
        for line in self.requesicion_line_ids:
            if line.partner_id.id == po.partner_id.id:
                vals = {
                    'product_id': line.product_id.id,
                    'name': line.description,
                    'product_qty': line.qty,
                    'price_unit': line.precio,
                    'order_id': po.id,
                    'taxes_id': line.tax_ids,
                    'account_analytic_id': line.cuenta_id.id
                }
                pol_env.sudo().create(vals)

    def providers_tuple(self):
        providers = []
        for line in self.requesicion_line_ids:
            proveedor = line.partner_id
            if proveedor.id not in providers:
                providers.append(proveedor.id)
        return providers

    def validaciones(self):
        if not self.requesicion_line_ids:
            raise UserError(_("Favor agregar lineas de Requisición antes de Generar Compras!"))

        for line in self.requesicion_line_ids:
            if not line.description:
                raise UserError(_("Falta Descripción de Linea"))

            if not line.partner_id:
                raise UserError(_("Falta Proveedor de Linea"))

            if line.precio == 0:
                raise UserError(_("Falta Precio de Linea"))

    def generar_compras(self):
        self.validaciones()
        po = []
        proveedores = self.providers_tuple()
        for id in proveedores:
            po_env = self.env['purchase.order']
            new_po = po_env.create({
                "partner_id": id,
                "requisicion_con_id": self.id,
            })
            po.append((4, new_po.id))
        self.purchase_ids = po

        for po in self.purchase_ids:
            self.create_POL(po)

        return self.action_view_purchase_orders()


