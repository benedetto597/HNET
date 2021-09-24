# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Registro de pago (Herencia - Contabilidad)
    @name_file account_payment_register_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
import datetime
from odoo import models, fields, api, _

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    PAYMENT_METHOD_SELECTION = [
        ('Efectivo', 'Efectivo'),  
        ('Tarjeta débito/crédito', 'Tarjeta débito/crédito'),              
        ('Transferencia bancaria', 'Transferencia bancaria'),
        ('Cheque', 'Cheque'),
    ]

    payment_method_selection = fields.Selection(
        PAYMENT_METHOD_SELECTION, string='Método de pago',
        required=True, index=True, copy=False)

    def action_create_payments(self):
        payments = super(AccountPaymentRegister, self).action_create_payments()
        return payments


    def _create_payment_vals_from_wizard(self):
        """
            Overwrite
            Cuando se registra el pago cargarlo a los pagos de la sesión de venta
        """
        payment_vals = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        
        account_move = self.env['account.move'].search([('name', '=', self.communication)])
        # account_move_payment = self.env['account.move'].search([('ref', '=', self.communication)])

        sale_order = self.env['sale.order'].search([('name', '=', account_move.invoice_origin)])

        # Crear el salesteam_payment de la orden actual
        salesteam_payment = self.env['salesteam.payment']   
           
        values = {
            'name': account_move.name,
            'sale_order_id': sale_order.id,
            'amount': self.amount,
            'payment_method_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'currency_rate': sale_order.currency_rate,
            'partner_id': self.partner_id.id,
            'salesteam_session_id': sale_order.salesteam_session_id.id,
            'company_id': sale_order.company_id.id,
            'transaction_id': account_move.id,
            'payment_status': 'paid'
        }

        salesteam_payment.create(values)

        return payment_vals