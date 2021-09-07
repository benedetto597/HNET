from odoo import fields, models


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    ai_email_tmpl_id = fields.Many2one('mail.template', string='Correo: Aprobación Ajuste Inventario')
