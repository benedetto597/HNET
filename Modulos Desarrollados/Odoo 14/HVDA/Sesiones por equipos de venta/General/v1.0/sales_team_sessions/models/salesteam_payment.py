# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Pagos para las sesiones de equipo de ventas
    @name_file salesteam_payment.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models, _
from odoo.tools import formatLang
from odoo.exceptions import ValidationError


class SalesTeamPayment(models.Model):
    """ Used to register payments made in a sale.order.

    See `payment_ids` field of sale.order model.
    The main characteristics of sale.payment can be read from
    `payment_method_id`.
    """

    _name = "salesteam.payment"
    _description = "Pagos por sesión de equipo de ventas"
    _order = "id desc"

    name = fields.Char(string='Registro', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Orden de Venta', required=True)
    amount = fields.Monetary(string='Monto', required=True, currency_field='currency_id', readonly=True, help="Total amount of the payment.")
    payment_method_id = fields.Many2one('account.journal', string='Método de Pago', required=True)
    payment_date = fields.Datetime(string='Fecha', required=True, readonly=True, default=lambda self: fields.Datetime.now())
    currency_id = fields.Many2one('res.currency', string='Moneda', related='sale_order_id.currency_id')
    currency_rate = fields.Float(string='Ratio de Conversión', related='sale_order_id.currency_rate', help='Conversion rate from company currency to order currency.')
    partner_id = fields.Many2one('res.partner', string='Cliebte', related='sale_order_id.partner_id')
    salesteam_session_id = fields.Many2one('salesteam.session', string='Sesión de venta', related='sale_order_id.salesteam_session_id', store=True, index=True)
    company_id = fields.Many2one('res.company', string='Compañía', related='sale_order_id.company_id')  # TODO: add store=True in master
    transaction_id = fields.Char('Transacción')
    payment_status = fields.Char('Estado del Pago')

    @api.model
    def create(self, values):
        salesteam_payment = super(SalesTeamPayment, self).create(values)
        return salesteam_payment
        
    @api.model
    def name_get(self):
        res = []
        for payment in self:
            if payment.name:
                res.append((payment.id, '%s %s' % (payment.name, formatLang(self.env, payment.amount, currency_obj=payment.currency_id))))
            else:
                res.append((payment.id, formatLang(self.env, payment.amount, currency_obj=payment.currency_id)))
        return res

    @api.constrains('payment_method_id')
    def _check_payment_method_id(self):
        for payment in self:
            print(payment.payment_method_id)
            print(payment.salesteam_session_id.config_id.payment_method_ids)
            if payment.payment_method_id not in payment.salesteam_session_id.config_id.payment_method_ids:
                raise ValidationError(_('El método de pago seleccionado no está permitido en la configuración de la sesión del equipo de venta.'))

    