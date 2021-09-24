# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Configuración para la sesión del equipo de ventas
    @name_file salesteam_config.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from datetime import datetime
from uuid import uuid4
import pytz

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

# ------------------------------------- CASHBOX -------------------------------------# 
class AccountBankStmtCashWizard(models.Model):
    _inherit = 'account.bank.statement.cashbox'

    @api.depends('salesteam_config_ids')
    @api.depends_context('current_currency_id')
    def _compute_currency(self):
        super(AccountBankStmtCashWizard, self)._compute_currency()
        for cashbox in self:
            if cashbox.salesteam_config_ids:
                cashbox.currency_id = cashbox.salesteam_config_ids[0].currency_id.id
            elif self.env.context.get('current_currency_id'):
                cashbox.currency_id = self.env.context.get('current_currency_id')

    salesteam_config_ids = fields.One2many('salesteam.config', 'default_cashbox_id')
    is_a_template = fields.Boolean(default=False)

    @api.model
    def default_get(self, fields):
        vals = super(AccountBankStmtCashWizard, self).default_get(fields)
        if 'cashbox_lines_ids' not in fields:
            return vals
        config_id = self.env.context.get('default_salesteam_id') # default_pos_id
        if config_id:
            config = self.env['salesteam.config'].browse(config_id)
            if config.last_session_closing_cashbox.cashbox_lines_ids:
                lines = config.last_session_closing_cashbox.cashbox_lines_ids
            else:
                lines = config.default_cashbox_id.cashbox_lines_ids
            if self.env.context.get('balance', False) == 'start':
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]
            else:
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': 0, 'subtotal': 0.0}] for line in lines]
        return vals

    def _validate_cashbox(self):
        super(AccountBankStmtCashWizard, self)._validate_cashbox()
        session_id = self.env.context.get('salesteam_session_id') 
        if session_id:
            current_session = self.env['salesteam.session'].browse(session_id)
            if current_session.state == 'new_session':
                current_session.write({'state': 'opening_control'})

    def set_default_cashbox_salesteam(self):
        self.ensure_one()
        current_session = self.env['salesteam.session'].browse(self.env.context['salesteam_session_id']) 
        lines = current_session.config_id.default_cashbox_id.cashbox_lines_ids
        context = dict(self._context)
        self.cashbox_lines_ids.unlink()
        self.cashbox_lines_ids = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]

        return {
            'name': _('Control de efectivo'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.bank.statement.cashbox',
            'view_id': self.env.ref('sales_team_sessions.view_account_bnk_stmt_cashbox_footer').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
            'res_id': self.id,
        }


# ------------------------------ Configuración Equipo de venta ------------------------------# 
class SalesTeamConfig(models.Model):
    _name = 'salesteam.config'
    _description = 'Sales Team Configuration'

    #### ------------------------------------- Valores por default para campos especificos ------------------------------------####
    #### ---------------------------------------------------------------------------------------------------------------------####
    def _default_picking_type_id(self):
        return self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1).buy_pull_id.id

    def _default_sale_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id), ('code', '=', 'INV')], limit=1)

    def _default_invoice_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id)], limit=1)

    def _default_pricelist(self):
        return self.env['product.pricelist'].search([('company_id', 'in', (False, self.env.company.id)), ('currency_id', '=', self.env.company.currency_id.id)], limit=1)
    
    def _default_payment_methods(self):
        return self.env['account.journal'].search([('company_id', '=', self.env.company.id), ('type', 'in', ('bank', 'cash', 'sale')), ('default_account_id', '>=', 1)])

    #### ------------------------------------------------- Campos del Modelo ------------------------------------------------ ####
    #### ---------------------------------------------------------------------------------------------------------------------####
    name = fields.Char(string='Configuración de la sesión del equipo de ventas', index=True, required=True, help="An internal identification of the point of sale.")
    is_installed_account_accountant = fields.Boolean(string="Esta instalada toda la contabilidad?",
        compute="_compute_is_installed_account_accountant")
    picking_type_id = fields.Many2one(
        'stock.picking.type',
        string='Tipoe de Operación',
        default=_default_picking_type_id,
        required=True,
        domain="[('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)]",
        ondelete='restrict')
    journal_id = fields.Many2one(
        'account.journal', string='Diario de ventas',
        domain=[('type', '=', 'sale')],
        help="Accounting journal used to post sales entries.",
        default=_default_sale_journal,
        ondelete='restrict')
    invoice_journal_id = fields.Many2one(
        'account.journal', string='Diario de facturas',
        domain=[('type', '=', 'sale')],
        help="Accounting journal used to create invoices.",
        default=_default_invoice_journal)
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', string="Moneda")
   # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
    iface_available_categ_ids = fields.Many2many('product.category', string='Categorias de productos disponibles',
        help='The point of sale will only display products which are within one of the selected category trees. If no category is specified, all available products will be shown')
    selectable_categ_ids = fields.Many2many('product.category', compute='_compute_selectable_categories')
    cash_control = fields.Boolean(string='Control de efectivo', help="Check the amount of the cashbox at opening and closing.", default=True)
   # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
    active = fields.Boolean(default=True)
    uuid = fields.Char(readonly=True, default=lambda self: str(uuid4()), copy=False,
        help='A globally unique identifier for this salesteam session configuration, used to prevent conflicts in client-generated data.')
    sequence_id = fields.Many2one('ir.sequence', string='Secuencia del identificador de ordenes', readonly=True,
        help="This sequence is automatically created by Odoo but you can change it "
        "to customize the reference numbers of your orders.", copy=False, ondelete='restrict')
    sequence_line_id = fields.Many2one('ir.sequence', string='Secuencia del identificador de las lineas de ordenes', readonly=True,
        help="This sequence is automatically created by Odoo but you can change it "
        "to customize the reference numbers of your orders lines.", copy=False)
    session_ids = fields.One2many('salesteam.session', 'config_id', string='Sesiones')
    current_session_id = fields.Many2one('salesteam.session', compute='_compute_current_session', string="Sesión Actual")
    current_session_state = fields.Char(compute='_compute_current_session')
    last_session_closing_cash = fields.Float(compute='_compute_last_session')
    last_session_closing_date = fields.Date(compute='_compute_last_session')
    last_session_closing_cashbox = fields.Many2one('account.bank.statement.cashbox', compute='_compute_last_session')
    salesteam_session_username = fields.Char(compute='_compute_current_session_user')
    salesteam_session_state = fields.Char(compute='_compute_current_session_user')
    salesteam_session_duration = fields.Char(compute='_compute_current_session_user')
    pricelist_id = fields.Many2one('product.pricelist', string='Lista de precios por defecto', required=True, default=_default_pricelist,
        help="The pricelist used if no customer is selected or if the customer has no Sale Pricelist configured.")
    available_pricelist_ids = fields.Many2many('product.pricelist', string='Lista de precios disponibles', default=_default_pricelist,
        help="Make several pricelists available in the Point of Sale. You can also apply a pricelist to specific customers from their contact form (in Sales tab). To be valid, this pricelist must be listed here as an available pricelist. Otherwise the default pricelist will apply.")
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)
    barcode_nomenclature_id = fields.Many2one('barcode.nomenclature', string='Nomenclatura de código de barras',
        help='Defines what kind of barcodes are available and how they are assigned to products, customers and cashiers.',
        default=lambda self: self.env.company.nomenclature_id, required=True)
   # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
    fiscal_position_ids = fields.Many2many('account.fiscal.position', string='Posición Fiscal', help='This is useful for restaurants with onsite and take-away services that imply specific tax rates.')
    default_fiscal_position_id = fields.Many2one('account.fiscal.position', string='Posición Fiscal por defecto')
    default_cashbox_id = fields.Many2one('account.bank.statement.cashbox', string='Balance por defecto')
    tax_regime = fields.Boolean("Tax Regime")
    tax_regime_selection = fields.Boolean("Valor del regimen de impuestos")
    module_account = fields.Boolean(string='Facturación', default=True, help='Enables invoice generation from the Sales Team Session.')
   # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
    amount_authorized_diff = fields.Float('Monto de diferencia autorizado',
        help="This field depicts the maximum difference allowed between the ending balance and the theoretical cash when "
             "closing a session, for non-SaleTeams managers. If this maximum is reached, the user will have an error message at "
             "the closing of his session saying that he needs to contact his manager.", default=0.00)
    payment_method_ids = fields.Many2many('account.journal', string='Métodos de pago', default=lambda self: self._default_payment_methods())
    company_has_template = fields.Boolean(string="La compañía tienen gráficos de cuentas", compute="_compute_company_has_template")
    current_user_id = fields.Many2one('res.users', string='Responsable de la sesión actual', compute='_compute_current_session_user')
    rounding_method = fields.Many2one('account.cash.rounding', string="Redondeo de efectivo")
    cash_rounding = fields.Boolean(string="Cash Rounding")
    only_round_cash_method = fields.Boolean(string="Solo aplicar rendondeo al efectivo")
    has_active_session = fields.Boolean(compute='_compute_current_session')
    manual_discount = fields.Boolean(string="Descuento manual", default=True)
    crm_team_id = fields.Many2one(
        'crm.team', string="Equipo de ventas",
        help="This Sales Team Session is related to this Sales Team.")

    #### ------------------------------------------------- Campos Calculados --------------------------------------------------####
    #### ---------------------------------------------------------------------------------------------------------------------####
    def _compute_is_installed_account_accountant(self):
        account_accountant = self.env['ir.module.module'].sudo().search([('name', '=', 'account_accountant'), ('state', '=', 'installed')])
        for salesteam_config in self:
            salesteam_config.is_installed_account_accountant = account_accountant and account_accountant.id

    @api.depends('iface_available_categ_ids')
    def _compute_selectable_categories(self):
        for config in self:
            if config.iface_available_categ_ids:
                config.selectable_categ_ids = config.iface_available_categ_ids
            else:
                config.selectable_categ_ids = self.env['product.category'].search([])

    @api.depends('journal_id.currency_id', 'journal_id.company_id.currency_id', 'company_id', 'company_id.currency_id')
    def _compute_currency(self):
        for salesteam_config in self:
            if salesteam_config.journal_id:
                salesteam_config.currency_id = salesteam_config.journal_id.currency_id.id or salesteam_config.journal_id.company_id.currency_id.id
            else:
                salesteam_config.currency_id = salesteam_config.company_id.currency_id.id

    @api.depends('session_ids', 'session_ids.state')
    def _compute_current_session(self):
        """If there is an open session, store it to current_session_id / current_session_State.
        """
        for salesteam_config in self:
            opened_sessions = salesteam_config.session_ids.filtered(lambda s: not s.state == 'closed')
            session = salesteam_config.session_ids.filtered(lambda s: not s.state == 'closed' and not s.rescue)
            # sessions ordered by id desc
            salesteam_config.has_active_session = opened_sessions and True or False
            salesteam_config.current_session_id = session and session[0].id or False
            salesteam_config.current_session_state = session and session[0].state or False

    @api.depends('session_ids')
    def _compute_last_session(self):
        SalesTeamSession = self.env['salesteam.session']
        for salesteam_config in self:
            session = SalesTeamSession.search_read(
                [('config_id', '=', salesteam_config.id), ('state', '=', 'closed')],
                ['cash_register_balance_end_real', 'stop_at', 'cash_register_id'],
                order="stop_at desc", limit=1)
            if session:
                timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
                salesteam_config.last_session_closing_date = session[0]['stop_at'].astimezone(timezone).date()
                if session[0]['cash_register_id']:
                    salesteam_config.last_session_closing_cash = session[0]['cash_register_balance_end_real']
                    salesteam_config.last_session_closing_cashbox = self.env['account.bank.statement'].browse(session[0]['cash_register_id'][0]).cashbox_end_id
                else:
                    salesteam_config.last_session_closing_cash = 0
                    salesteam_config.last_session_closing_cashbox = False
            else:
                salesteam_config.last_session_closing_cash = 0
                salesteam_config.last_session_closing_date = False
                salesteam_config.last_session_closing_cashbox = False

    @api.depends('session_ids')
    def _compute_current_session_user(self):
        for salesteam_config in self:
            session = salesteam_config.session_ids.filtered(lambda s: s.state in ['opening_control', 'opened', 'closing_control'] and not s.rescue)
            if session:
                salesteam_config.salesteam_session_username = session[0].user_id.sudo().name
                salesteam_config.salesteam_session_state = session[0].state
                salesteam_config.salesteam_session_duration = (
                    datetime.now() - session[0].start_at
                ).days if session[0].start_at else 0
                salesteam_config.current_user_id = session[0].user_id
            else:
                salesteam_config.salesteam_session_username = False
                salesteam_config.salesteam_session_state = False
                salesteam_config.salesteam_session_duration = 0
                salesteam_config.current_user_id = False

    @api.depends('company_id')
    def _compute_company_has_template(self):
        for config in self:
            if config.company_id.chart_template_id:
                config.company_has_template = True
            else:
                config.company_has_template = False

    #### ------------------------------------------ Campos con rastreo de cambios -------------------------------------------- ####
    #### ---------------------------------------------------------------------------------------------------------------------####

    @api.onchange('company_id')
    def _get_default_sales_team(self):
        default_sale_team = self.env.ref('default_salesteam_config', raise_if_not_found=False)
        if default_sale_team and (not default_sale_team.company_id or default_sale_team.company_id == self.company_id):
            self.crm_team_id = default_sale_team
        else:
            self.crm_team_id = self.env['crm.team'].search(['|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)], limit=1)

    @api.onchange('iface_print_via_proxy')
    def _onchange_iface_print_via_proxy(self):
        self.iface_print_auto = self.iface_print_via_proxy
        if not self.iface_print_via_proxy:
            self.iface_cashdrawer = False

    @api.onchange('module_account')
    def _onchange_module_account(self):
        if self.module_account and not self.invoice_journal_id:
            self.invoice_journal_id = self._default_invoice_journal()
    
    @api.onchange('tax_regime')
    def _onchange_tax_regime(self):
        if not self.tax_regime:
            self.default_fiscal_position_id = False

    @api.onchange('tax_regime_selection')
    def _onchange_tax_regime_selection(self):
        if not self.tax_regime_selection:
            self.fiscal_position_ids = [(5, 0, 0)]

    @api.onchange('available_pricelist_ids')
    def _onchange_available_pricelist_ids(self):
        if self.pricelist_id not in self.available_pricelist_ids._origin:
            self.pricelist_id = False

    #### ----------------------------- Revisión de campos previo a apertura | cierre de sesión ------------------------------ ####
    #### ---------------------------------------------------------------------------------------------------------------------####
    @api.constrains('cash_control')
    def _check_session_state(self):
        open_session = self.env['salesteam.session'].search([('config_id', '=', self.id), ('state', '!=', 'closed')])
        if open_session:
            raise ValidationError(_("No se le permite cambiar el estado de control de efectivo mientras una sesión ya está abierta."))

    @api.constrains('company_id', 'journal_id')
    def _check_company_journal(self):
        if self.journal_id and self.journal_id.company_id.id != self.company_id.id:
            raise ValidationError(_("El diario de ventas y la sesión del equipo de ventas deben pertenecer a la misma empresa."))

    def _check_profit_loss_cash_journal(self):
        if self.cash_control and self.payment_method_ids:
            for method in self.payment_method_ids:
                #if method.is_cash_count and (not method.cash_journal_id.loss_account_id or not method.cash_journal_id.profit_account_id):
                if method.type == 'cash' and (not method.loss_account_id or not method.profit_account_id):
                    raise ValidationError(_("Necesita una cuenta de pérdidas y ganancias en su diario de caja."))

    @api.constrains('company_id', 'invoice_journal_id')
    def _check_company_invoice_journal(self):
        if self.invoice_journal_id and self.invoice_journal_id.company_id.id != self.company_id.id:
            raise ValidationError(_("El diario de facturas y el equipo de ventas deben pertenecer a la misma empresa."))

    @api.constrains('company_id', 'payment_method_ids')
    def _check_company_payment(self):
        if self.env['account.journal'].search_count([('id', 'in', self.payment_method_ids.ids), ('company_id', '!=', self.company_id.id)]):
            raise ValidationError(_("Los métodos de pago y el equipo de ventas deben pertenecer a la misma empresa."))

    def _check_modules_to_install(self):
        # determine modules to install
        expected = [
            fname[7:]           # 'module_account' -> 'account'
            for fname in self.fields_get_keys()
            if fname.startswith('module_')
            if any(salesteam_config[fname] for salesteam_config in self)
        ]
        if expected:
            STATES = ('installed', 'to install', 'to upgrade')
            modules = self.env['ir.module.module'].sudo().search([('name', 'in', expected)])
            modules = modules.filtered(lambda module: module.state not in STATES)
            if modules:
                modules.button_immediate_install()
                # just in case we want to do something if we install a module. (like a refresh ...)
                return True
        return False

    @api.constrains('payment_method_ids')
    def _check_payment_method_receivable_accounts(self):
        # This is normally not supposed to happen to have a payment method without a receivable account set,
        # as this is a required field. However, it happens the receivable account cannot be found during upgrades
        # and this is a bommer to block the upgrade for that point, given the user can correct this by himself,
        # without requiring a manual intervention from our upgrade support.
        # However, this must be ensured this receivable is well set before opening a POS session.
        invalid_payment_methods = self.payment_method_ids.filtered(lambda method: not method.default_account_id) 
        if invalid_payment_methods:
            method_names = ", ".join(method.name for method in invalid_payment_methods)
            raise ValidationError(
                _("Debes configurar una cuenta intermediaria para los métodos de pago: %s.") % method_names
            )

    def _check_payment_method_ids(self):
        self.ensure_one()
        if not self.payment_method_ids:
            raise ValidationError(
                _("Debe tener al menos un método de pago configurado para iniciar una sesión.")
            )
    
    @api.constrains('rounding_method')
    def _check_rounding_method_strategy(self):
        if self.cash_rounding and self.rounding_method.strategy != 'add_invoice_line':
            raise ValidationError(_("La estrategia de redondeo de efectivo debe ser: 'Agregar una línea de redondeo'"))

    @api.constrains('company_id', 'available_pricelist_ids')
    def _check_companies(self):
        if any(self.available_pricelist_ids.mapped(lambda pl: pl.company_id.id not in (False, self.company_id.id))):
            raise ValidationError(_("Las listas de precios seleccionadas no deben pertenecer a ninguna empresa ni a la empresa del equipo de venta."))

    def _check_groups_implied(self):
        for salesteam_config in self:
            for field_name in [f for f in salesteam_config.fields_get_keys() if f.startswith('group_')]:
                field = salesteam_config._fields[field_name]
                if field.type in ('boolean', 'selection') and hasattr(field, 'implied_group'):
                    field_group_xmlids = getattr(field, 'group', 'base.group_user').split(',')
                    field_groups = self.env['res.groups'].concat(*(self.env.ref(it) for it in field_group_xmlids))
                    field_groups.write({'implied_ids': [(4, self.env.ref(field.implied_group).id)]})

    @api.constrains('pricelist_id', 'available_pricelist_ids', 'journal_id', 'invoice_journal_id', 'payment_method_ids')
    def _check_currencies(self):
        for config in self:
            if config.pricelist_id not in config.available_pricelist_ids:
                raise ValidationError(_("The default pricelist must be included in the available pricelists."))
        if any(self.available_pricelist_ids.mapped(lambda pricelist: pricelist.currency_id != self.currency_id)):
            raise ValidationError(_("Todas las listas de precios disponibles deben estar en la misma moneda que la empresa o"
                                    " como el diario de ventas establecido en este equipo de venta si utiliza"
                                    " la aplicación Contabilidad."))
        if self.invoice_journal_id.currency_id and self.invoice_journal_id.currency_id != self.currency_id:
            raise ValidationError(_("El diario de facturas debe estar en la misma moneda que el diario de ventas o la moneda de la empresa si no se establece."))
        if any(
            self.payment_method_ids\
                .filtered(lambda pm: pm.type == 'cash')\
                .mapped(lambda pm: self.currency_id not in self.company_id.currency_id )
        ):
            raise ValidationError(_("Todos los métodos de pago deben estar en la misma moneda que el Diario de ventas o la moneda de la empresa si no se establece."))
    #### ---------------------------------------- Apertura | Cierre de sesión de ventas ------------------------------------- ####
    #### ---------------------------------------------------------------------------------------------------------------------####
    def open_session_cb(self, crm_team, selected_user, check_coa=True):
        """ new session button

        create one if none exist
        access cash control interface if enabled or start a session
        """
        self.ensure_one()
        if not self.current_session_id:
            self._check_company_journal()
            self._check_company_invoice_journal()
            self._check_company_payment()
            self._check_currencies()
            self._check_profit_loss_cash_journal()
            self._check_payment_method_ids()
            self._check_payment_method_receivable_accounts()
            self.env['salesteam.session'].create({
                'user_id': selected_user,
                'config_id': self.id,
                'crm_team_id': crm_team
            })
                
    def open_existing_session_cb(self):
        """ close session button

        access session form to validate entries
        """
        self.ensure_one()
        
        return self._open_session(self.current_session_id.id)

    def _open_session(self, session_id):
        domain = []
        res_id = session_id
        search_action = self.env.ref('sales_team_sessions.action_sales_team_session').read()[0]
        res = dict(search_action, domain=domain, res_id=res_id)
        return res
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'salesteam.session.form.view',
            'res_model': 'salesteam.session',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': session_id,
            'view_id': 'view_salesteam_session_form',
        }
        """

    def execute(self):
        return {
             'type': 'ir.actions.client',
             'tag': 'reload',
             'params': {'wait': True}
         }

    #### ---------------------------------- CREACION | MODIFICACION | ELIMINADO de Registro --------------------------------- ####
    #### ---------------------------------------------------------------------------------------------------------------------####
    def name_get(self):
        result = []
        for config in self:
            last_session = self.env['salesteam.session'].search([('config_id', '=', config.id)], limit=1)
            if (not last_session) or (last_session.state == 'closed'):
                result.append((config.id, _("%(salesteam_conf_name)s (not used)", salesteam_conf_name=config.name)))
            else:
                result.append((config.id, "%s (%s)" % (config.name, last_session.user_id.name)))
        return result

    @api.model
    def create(self, values):
        IrSequence = self.env['ir.sequence'].sudo()
        val = {
            'name': _('Sales Team Order %s', values['name']),
            'padding': 4,
            'prefix': "%s/" % values['name'],
            'code': "salesteam.order",
            'company_id': values.get('company_id', False),
        }
        # force sequence_id field to new salesteam.order sequence
        values['sequence_id'] = IrSequence.create(val).id

        val.update(name=_('Sale Team Order line %s', values['name']), code='salesteam.orderline')
        values['sequence_line_id'] = IrSequence.create(val).id
        salesteam_config = super(SalesTeamConfig, self).create(values)
        salesteam_config.sudo()._check_modules_to_install()
        salesteam_config.sudo()._check_groups_implied()
        # If you plan to add something after this, use a new environment. The one above is no longer valid after the modules install.
        return salesteam_config

    def write(self, vals):
        opened_session = self.mapped('session_ids').filtered(lambda s: s.state != 'closed')
        if opened_session:
            forbidden_fields = []
            for key in self._get_forbidden_change_fields():
                if key in vals.keys():
                    field_name = self._fields[key].get_description(self.env)["string"]
                    forbidden_fields.append(field_name)
            if len(forbidden_fields) > 0:
                raise UserError(_(
                    "No se puede modificar esta configuración de PoS porque no se puede modificar %s mientras una sesión está abierta.",
                    ", ".join(forbidden_fields)
                ))
        result = super(SalesTeamConfig, self).write(vals)

        self.sudo()._set_fiscal_position()
        self.sudo()._check_modules_to_install()
        self.sudo()._check_groups_implied()
        return result

    def _get_forbidden_change_fields(self):
        forbidden_keys = ['cash_control', 'available_pricelist_ids', 'iface_available_categ_ids',
                        'payment_method_ids']
        return forbidden_keys

    def unlink(self):
        # Delete the pos.config records first then delete the sequences linked to them
        sequences_to_delete = self.sequence_id | self.sequence_line_id
        res = super(SalesTeamConfig, self).unlink()
        sequences_to_delete.unlink()
        return res

    def _set_fiscal_position(self):
        for config in self:
            if config.tax_regime and config.default_fiscal_position_id.id not in config.fiscal_position_ids.ids:
                config.fiscal_position_ids = [(4, config.default_fiscal_position_id.id)]
            elif not config.tax_regime_selection and not config.tax_regime and config.fiscal_position_ids.ids:
                config.fiscal_position_ids = [(5, 0, 0)]