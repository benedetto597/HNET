from odoo import fields, models, api, _
from odoo.exceptions import UserError

LEVELS = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4')]


class PinForApprovalWizard(models.TransientModel):
    _name = 'pin.for.approval.wizard'

    pin = fields.Char(string="PIN")
    levels = fields.Selection(selection=LEVELS, string='Niveles')
    level = fields.Integer(string='Nivel a Aprobar')
    purchase_order_id = fields.Many2one('purchase.order', string="Orden de Compra")

    def action_po_approve(self):
        if not self.pin:
            raise UserError(_("Favor Ingresar PIN antes de Aprobar"))

        employee = self.env.user.employee_id
        if not employee:
            raise UserError(_("Favor contactar a adminstración para que vincule su usuario a un perfil de empleado."))

        if self.pin != employee.pin:
            raise UserError(_("PIN INCORRECTO!"))
        else:
            po = self.purchase_order_id
            nivel_aprov = self.level_approve(po)
            if po.confirm_ready:
                po.state = "ready"
            else:
                po.state = "approver_%s" % nivel_aprov
                self.purchase_order_id.send_email_next(nivel=nivel_aprov)

    def level_approve(self, po):
        if self.level == 1:
            po.app_1 = True
            po.approve_1_id = self.env.user.id
            po.approver_1_date = fields.Datetime.now()
            return 2

        elif self.level == 2:
            po.app_2 = True
            po.approve_2_id = self.env.user.id
            po.approver_2_date = fields.Datetime.now()
            return 3

        elif self.level == 3:
            po.app_3 = True
            po.approve_3_id = self.env.user.id
            po.approver_3_date = fields.Datetime.now()
            return 4

        elif self.level == 4:
            po.app_4 = True
            po.approve_4_id = self.env.user.id
            po.approver_4_date = fields.Datetime.now()
            return 4









