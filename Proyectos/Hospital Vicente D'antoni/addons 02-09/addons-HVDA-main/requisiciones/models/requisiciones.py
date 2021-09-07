from odoo import models, fields, api, _
from odoo.exceptions import UserError

TIPO = [('abastecimiento', 'Abastecimiento'), ('gasto', 'Gasto')]
ESTADO = [('draft', 'Borrador'), ('done', 'Confirmado'), ('condensado', 'Condensado')]


class Requisiciones(models.Model):
    _name = 'requisicion'
    _description = 'requisicion'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), track_visibility='onchange')
    type = fields.Selection(TIPO, default='gasto', index=True, required=True)
    state = fields.Selection(ESTADO, default='draft', string="Estado")
    department_id = fields.Many2one('hr.department', string='Departmento', compute='get_departament_id')
    requesicion_line_ids = fields.One2many(comodel_name="requisicion.lineas", inverse_name="requisicion_id")
    condensado = fields.Boolean(string="Fue Condensado")
    date = fields.Date(string="Fecha", default=fields.Date.context_today)
    currency_id = fields.Many2one('res.currency', string="Moneda",
                                  default=lambda self: self.env.user.company_id.currency_id)
    note = fields.Text('Notas')
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
            if vals.get('type') == 'abastecimiento':
                vals['name'] = self.env['ir.sequence'].next_by_code('ra.sequence') or _('New')

            elif vals.get('type') == 'gasto':
                vals['name'] = self.env['ir.sequence'].next_by_code('rg.sequence') or _('New')

            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('requisicion.sequence') or _('New')

        result = super(Requisiciones, self).create(vals)
        return result

    @api.depends('create_uid')
    def get_departament_id(self):
        for rec in self:
            if rec.create_uid and rec.create_uid.department_id:
                rec.department_id = rec.create_uid.department_id.id
            else:
                rec.department_id = False

    def check_state(self):
        for rec in self:
            if rec.state != "done":
                raise UserError(_("Todas las requisiciones tienen que estar confirmadas"))

    def condensar_requisiciones(self):
        requisiciones = []
        requisiciones_condensadas = self.env['requisiciones.condensadas']
        self.check_state()
        for rec in self:
            for line in rec.requesicion_line_ids:
                requisiciones.append((4, line.id))
        self.state = "condensado"
        req_con = requisiciones_condensadas.create({
            'requesicion_line_ids': requisiciones
            })

        return {'type': 'ir.actions.act_window',
                'res_model': 'requisiciones.condensadas',
                'views': [[self.env.ref('requisiciones.requisicion_condensada_form_view').id, 'form']],
                'view_mode': 'form',
                'res_id': req_con.id}

    def validaciones(self):
        if not self.requesicion_line_ids:
            raise UserError(_("Agregue lineas de requisicion antes de confirmar!"))

        for line in self.requesicion_line_ids:
            if not line.product_id:
                raise UserError(_("Falta Producto de Linea"))

            if not line.description:
                raise UserError(_("Falta Descripción de Linea"))

            if not line.location_id:
                raise UserError(_("Falta Ubicación de Linea"))

            if not line.qty:
                raise UserError(_("Falta Cantidad de Linea"))

    def is_confirmed(self):
        self.state = "done"
        self.validaciones()
        return True

    def change_to_draft(self):
        self.state = "draft"
        return True


# lineas de la requisicion
class RequisicionLineas(models.Model):
    _name = 'requisicion.lineas'
    _description = 'requisicion.lineas'

    requisicion_id = fields.Many2one(comodel_name="requisicion", string="Requisicion")
    requisicion_con_id = fields.Many2one(comodel_name="requisiciones.condensadas", string="Requesicion Condensada")
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    qty = fields.Float(string="Cantidad")
    product_uom_id = fields.Many2one('uom.uom', string='Medida')
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')
    precio = fields.Monetary(string='Precio')
    cuenta_id = fields.Many2one('account.analytic.account', string="Cuenta Analitica")
    location_id = fields.Many2one("stock.location", "Ubicación")
    partner_id = fields.Many2one('res.partner', "Proveedor")
    currency_id = fields.Many2one('res.currency', string="Moneda")
    total = fields.Monetary(string='Total', compute="_get_total")
    description = fields.Char(string='Descripción')
    tax_ids = fields.Many2many(comodel_name="account.tax", inverse_name="requisicion_lin_id")
    type = fields.Selection(TIPO, related='requisicion_id.type', string="tipo")

    @api.model
    def create(self, vals):
        result = super(RequisicionLineas, self).create(vals)
        if result.requisicion_id:
            result.currency_id = result.requisicion_id.currency_id.id

        return result

    @api.depends('qty', 'precio')
    def _get_total(self):
        for rec in self:
            rec.total = rec.qty * rec.precio

    @api.onchange('type')
    def product_id_domain(self):
        for rec in self:
            domain = []
            if rec.type == 'gasto':
                domain = [('product_tmpl_id.gasto_chk', '=', True)]
            return {'domain': {'product_id': domain}}

    @api.onchange('product_id')
    def product_id_onchange(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id
            self.description = self.product_id.name
            self.tax_ids = [(5, 0, 0)]
            taxes = []
            for tax in self.product_id.taxes_id:
                taxes.append((4, tax.id))

            self.tax_ids = taxes

    @api.onchange('location_id')
    def location_id_onchange(self):
        if self.location_id and self.location_id.cuenta_id:
            self.cuenta_id = self.location_id.cuenta_id.id
        else:
            self.cuenta_id = False

    @api.onchange('requisicion_id.currency_id')
    def currency_id_onchange(self):
        if self.requisicion_id:
            self.currency_id = self.requisicion_id.currency_id.id
