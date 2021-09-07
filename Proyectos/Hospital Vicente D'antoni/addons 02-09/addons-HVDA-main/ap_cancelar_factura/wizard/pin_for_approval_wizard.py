from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PinAccountMoveWizard(models.TransientModel):
    _name = 'account.move.approval'

    pin = fields.Char(string="PIN")
    account_move_id = fields.Many2one('account.move', string="Account Move")

    def action_po_approve(self):
        if not self.pin:
            raise UserError(_("Favor Ingresar PIN antes de Aprobar"))

        employee = self.env.user.employee_id
        if not employee:
            raise UserError(_("Favor contactar a adminstración para que vincule su usuario a un perfil de empleado."))

        if self.pin != employee.pin:
            raise UserError(_("PIN INCORRECTO!"))
        else:
            am = self.account_move_id
            if am.state != "draft":
                am.button_draft()
            am.button_cancel()







