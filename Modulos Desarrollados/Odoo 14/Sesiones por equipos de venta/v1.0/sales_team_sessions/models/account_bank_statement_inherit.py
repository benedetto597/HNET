# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Estado o extracto bancario (Herencia - Contabilidad)
    @name_file account_bank_statement_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    salesteam_session_id = fields.Many2one('salesteam.session', string="Sales Team Session", copy=False)
    account_id = fields.Many2one('account.account', related='journal_id.default_account_id', readonly=True)

    def button_validate_or_action(self):
        # OVERRIDE to check the consistency of the statement's state regarding the session's state.
        for statement in self:
            if statement.salesteam_session_id.state  in ('opened', 'closing_control') and statement.state == 'open':
                raise UserError(_("No puede validar un extracto bancario que se utiliza en una sesión abierta de un equipo de ventas."))
        return super(AccountBankStatement, self).button_validate_or_action()

    def unlink(self):
        for bs in self:
            if bs.salesteam_session_id:
                raise UserError(_("No puede eliminar un extracto bancario vinculado a la sesión del equipo de ventas."))
        return super( AccountBankStatement, self).unlink()