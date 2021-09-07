# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    four_step_validation = fields.Boolean('Aprobación de Cuatro Niveles')

    approver_1_amount = fields.Monetary('Monto Gerente Adminsitrativo', default=0.0)
    approver_2_amount = fields.Monetary('Monto Contralor', default=0.0)
    approver_3_amount = fields.Monetary('Monto Director Ejecutivo', default=0.0)
    approver_4_amount = fields.Monetary('Presidente de la Junta Directiva', default=0.0)

    email_template_id = fields.Many2one('mail.template', string='Correo: Solicitud de Aprobación de Compra')
    refuse_template_id = fields.Many2one('mail.template', string='Correo: Rechazo de Compra')

