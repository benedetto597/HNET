# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Modelo trasendiente para la apertura, cierre y control de caja
    @name_file salesteam_box.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from typing import DefaultDict
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CashBox(models.TransientModel):
    _register = False

    name = fields.Char(string='Razón', required=True)
    # Attention, we don't set a domain, because there is a journal_type key
    # in the context of the action
    amount = fields.Float(string='Monto', digits=0, required=True)
    # Definir si es entrada o salida de efectivo
    is_in_or_out = fields.Selection([('in', 'Entrada de efectivo'), ('out', 'Salida de efectivo')], string="Entrada o Salida", required=True)

    def run(self):
        context = dict(self._context or {})
        active_model = context.get('active_model', False)
        active_ids = context.get('active_ids', [])

        records = self.env[active_model].browse(active_ids)

        return self._run(records)

    def _run(self, records):
        for box in self:
            for record in records:
                if not record.journal_id:
                    raise UserError(_("Verifique que el campo 'Diario' esté configurado en el extracto bancario"))
                if not record.journal_id.company_id.transfer_account_id:
                    raise UserError(_("Verifique que el campo 'Transferir cuenta' esté configurado en la empresa."))
                box._create_bank_statement_line(record)
        return {}

    def _create_bank_statement_line(self, record):
        for box in self:
            if record.state == 'confirm':
                raise UserError(_("No puede ingresar / retirar dinero para un extracto bancario que esté cerrado."))
            values = box._calculate_values_for_statement_line(record)
            account = record.journal_id.company_id.transfer_account_id
            self.env['account.bank.statement.line'].with_context(counterpart_account_id=account.id).create(values)


class CashBoxOut(CashBox):
    _name = 'cash.box.out.salesteam'
    _description = 'Cash Box Out'


    def _calculate_values_for_statement_line(self, record):
        if not record.journal_id.company_id.transfer_account_id:
            raise UserError(_("Debe definir una 'Cuenta de transferencia interna' en el diario de su caja registradora."))
        
        if not self.is_in_or_out:
            raise UserError(_("Tiene que definir si es entrada o salida de efectivo"))

        if self.is_in_or_out == 'in':
            # Entrar efectivo a caja
            amount = self.amount
        elif self.is_in_or_out == 'out':
            # Sacar Efectivo de caja
            amount = -self.amount

        return {
            'date': record.date,
            'statement_id': record.id,
            'journal_id': record.journal_id.id,
            'amount': amount,
            'payment_ref': self.name,
        }

class SalesTeamBox(CashBox):
    _register = False

    def run(self):
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'salesteam.session':
            bank_statements = [session.cash_register_id for session in self.env[active_model].browse(active_ids) if session.cash_register_id]
            if not bank_statements:
                raise UserError(_("No hay caja registradora para esta sesión del equipo de ventas"))
            return self._run(bank_statements)
        else:
            return super(SalesTeamBox, self).run()


class SalesTeamBoxOut(SalesTeamBox):
    _inherit = 'cash.box.out.salesteam'

    def _calculate_values_for_statement_line(self, record):
        values = super(SalesTeamBoxOut, self)._calculate_values_for_statement_line(record)
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'salesteam.session' and active_ids:
            values['ref'] = self.env[active_model].browse(active_ids)[0].name
        return values
