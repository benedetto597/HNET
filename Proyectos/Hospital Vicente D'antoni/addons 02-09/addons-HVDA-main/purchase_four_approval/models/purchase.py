from odoo import fields, models, api, _
from odoo.exceptions import UserError

EXTRA_STATUS = [
    ('approver_1', 'Esperando Aprobación Gerente Adminsitrativo'),
    ('approver_2', 'Esperando Aprobación Contralor'),
    ('approver_3', 'Esperando Aprobación Director Ejecutivo'),
    ('approver_4', 'Esperando Aprobación Presidente de la Junta Directiva'),
    ('ready', 'Listo Para Confirmar'),
    ('refuse', 'Rechazado')]

LEVELS = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4')]


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Other Fields
    state = fields.Selection(selection_add=EXTRA_STATUS, string='Status')
    levels = fields.Selection(selection=LEVELS, string='Niveles', compute="_get_level", store=True, copy=False)

    # User Fields
    approve_1_id = fields.Many2one('res.users', string='Gerente Adminsitrativo', readonly=True, copy=False)
    approve_2_id = fields.Many2one('res.users', string='Contralor', readonly=True, copy=False)
    approve_3_id = fields.Many2one('res.users', string='Director Ejecutivo', readonly=True, copy=False)
    approve_4_id = fields.Many2one('res.users', string='Presidente de la Junta Directiva', readonly=True, copy=False)
    purchase_user_id = fields.Many2one('res.users', string='Usuario de Compra', compute='_set_purchase_user', store=True, copy=False)

    # Refuse Fields
    po_refuse_user_id = fields.Many2one('res.users', string="Rechazado Por", readonly=True, copy=False)
    po_refuse_date = fields.Date(string="Fecha de Rechazo", readonly=True, copy=False)
    refuse_reason_note = fields.Text(string="Motivo de Rechazo", readonly=True, copy=False)

    # Date Fields
    approver_1_date = fields.Datetime(string='Gerente Adminsitrativo Aprobo el', readonly=True, copy=False)
    approver_2_date = fields.Datetime(string='Contralor Aprobo el', readonly=True, copy=False)
    approver_3_date = fields.Datetime(string='Director Ejecutivo Aprobo el', readonly=True, copy=False)
    approver_4_date = fields.Datetime(string='Presidente de la Junta Directiva Aprobo el', readonly=True, copy=False)

    # approved levels Fields
    confirm_ready = fields.Boolean('Listo para confirmar', compute="_get_confirm_ready", copy=False)
    hide_for_approval = fields.Boolean('Ocultar solicitar Aprobación', copy=False)
    app_1 = fields.Boolean('Approved 1', copy=False)
    app_2 = fields.Boolean('Approved 2', copy=False)
    app_3 = fields.Boolean('Approved 3', copy=False)
    app_4 = fields.Boolean('Approved 4', copy=False)

    # COMPUTED FIELD FUNCTIONS
    @api.depends('state')
    def _set_purchase_user(self):
        for rec in self:
            if rec.state == 'draft' or 'sent':
                rec.purchase_user_id = self.env.user.id,

    @api.depends('amount_total')
    def _get_level(self):
        for rec in self:
            rec.levels = rec.calculate_level()

    @api.depends('levels')
    def _get_confirm_ready(self):
        for rec in self:
            level = rec.levels
            rec.confirm_ready = rec.check_readiness(level)

    # ADITTIONAL FUNCTIONS
    def check_if_approval(self):
        """funcion para revisar si esta activo opcion de niveles de aprobacion"""
        must_approve = self.env.user.company_id.four_step_validation
        return must_approve

    def calculate_level(self):
        total = self.amount_total
        must_approve = self.check_if_approval()
        amount1 = self._get_approver_amount(1)
        amount2 = self._get_approver_amount(2)
        amount3 = self._get_approver_amount(3)
        amount4 = self._get_approver_amount(4)

        if must_approve:
            if amount1 <= total < amount2:
                return "1"
            elif amount2 <= total < amount3:
                return "2"
            elif amount3 <= total < amount4:
                return "3"
            elif total >= amount4:
                return "4"

        return "0"

    def _get_approver_amount(self, level):
        amount = False
        if level == 1:
            amount = self.env.user.company_id.approver_1_amount
        elif level == 2:
            amount = self.env.user.company_id.approver_2_amount
        elif level == 3:
            amount = self.env.user.company_id.approver_3_amount
        elif level == 4:
            amount = self.env.user.company_id.approver_4_amount
        return amount

    def check_readiness(self, level):
        app_1 = self.app_1
        app_2 = self.app_2
        app_3 = self.app_3
        app_4 = self.app_4
        if level == "0":
            return True
        elif level == "1":
            return app_1
        elif level == "2":
            return app_1 and app_2
        elif level == "3":
            return app_1 and app_2 and app_3
        elif level == "4":
            return app_1 and app_2 and app_3 and app_4

    # INHERITED FUNCTIONS
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'ready']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    # BTN FUNCTIONS
    def for_approval(self):
        self.hide_for_approval = True
        self.state = "approver_1"
        self.send_email_next(nivel=1)

    def app1(self):
        return self.get_pin_wiz(level=1)

    def app2(self):
        return self.get_pin_wiz(level=2)

    def app3(self):
        return self.get_pin_wiz(level=3)

    def app4(self):
        return self.get_pin_wiz(level=4)

    def get_pin_wiz(self, level):
        wizard_form = self.env.ref('purchase_four_approval.pin_for_approval_wiz_form', False)
        wiz_model_id = self.env['pin.for.approval.wizard']
        vals = {
            'levels': self.levels,
            'level': level,
            'purchase_order_id': self.id,
        }
        new = wiz_model_id.create(vals)

        return {
            'name': _('Aprobar Compra'),
            'type': 'ir.actions.act_window',
            'res_model': 'pin.for.approval.wizard',
            'res_id': new.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }

    def send_email_next(self, nivel):
        user_group = self.env.ref("purchase_four_approval.approver_%s_group" % nivel)
        users_emails = self.get_email_to(user_group)
        approv_template_id = self._get_approv_template_id()
        ctx = self._context.copy()
        ctx.update({'email_to': users_emails})
        if approv_template_id:
            approv_template_id.with_context(ctx).send_mail(self.id)
        return True

    def get_email_to(self, user_group):
        email_list = [
            usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        return ",".join(email_list)

    def _get_approv_template_id(self):
        return self.env.user.company_id.email_template_id

    def _get_refuse_template_id(self):
        return self.env.user.company_id.refuse_template_id
