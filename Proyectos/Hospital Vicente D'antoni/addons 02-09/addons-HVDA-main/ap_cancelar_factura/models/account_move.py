from odoo import models, fields, api, _


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def pin_button_cancel(self):
        return self.get_pin_wiz()

    def get_pin_wiz(self):
        wizard_form = self.env.ref('ap_cancelar_factura.pin_for_approval_am_form', False)
        wiz_model_id = self.env['account.move.approval']
        vals = {
            'account_move_id': self.id,
        }
        new = wiz_model_id.create(vals)

        return {
            'name': _('Aprobación Cancelar Factura'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.approval',
            'res_id': new.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }
