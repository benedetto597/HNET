# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Modelo trasendiente para la Apertura de caja 
    @name_file salesteam_open_statement.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, models, _
from odoo.exceptions import UserError


class SalesTeamOpenStatement(models.TransientModel):
    _name = 'salesteam.open.statement'
    _description = 'Estado de apertura de la caja de sesión de ventas'

    def open_statement(self):
        """ 
            Apertura de caja y registro contable en el estado de banco
        """
        self.ensure_one()
        BankStatement = self.env['account.bank.statement']
        journals = self.env['account.journal'].search([('journal_user', '=', True)])
        if not journals:
            raise UserError(_('Debe definir qué método de pago debe estar disponible en el punto de venta reutilizando el banco y el efectivo existentes a través de "Contabilidad / Configuración / Diarios / Diarios".'))

        for journal in journals:
            if journal.sequence_id:
                number = journal.sequence_id.next_by_id()
            else:
                raise UserError(_("No sequence defined on the journal"))
            BankStatement += BankStatement.create({'journal_id': journal.id, 'user_id': self.env.uid, 'name': number})

        tree_id = self.env.ref('account.view_bank_statement_tree').id
        form_id = self.env.ref('account.view_bank_statement_form').id
        search_id = self.env.ref('account.view_bank_statement_search').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Registro de efectivo'),
            'view_mode': 'tree,form',
            'res_model': 'account.bank.statement',
            'domain': str([('id', 'in', BankStatement.ids)]),
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'search_view_id': search_id,
        }
