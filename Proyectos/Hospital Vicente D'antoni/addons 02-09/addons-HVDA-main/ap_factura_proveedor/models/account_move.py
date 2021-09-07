from odoo import models, fields, api, _


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    po_id = fields.Many2one('purchase.order', string='Orden de Compra', readonly=True)

    def pin_action_post(self):
        return self.get_pin_wiz()

    def get_pin_wiz(self):
        wizard_form = self.env.ref('ap_factura_proveedor.pin_for_approval_amp_form', False)
        wiz_model_id = self.env['account.move.proveedor.approval']
        vals = {
            'account_move_id': self.id,
        }
        new = wiz_model_id.create(vals)

        return {
            'name': _('Aprobación Factura Proveedor'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.proveedor.approval',
            'res_id': new.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }
