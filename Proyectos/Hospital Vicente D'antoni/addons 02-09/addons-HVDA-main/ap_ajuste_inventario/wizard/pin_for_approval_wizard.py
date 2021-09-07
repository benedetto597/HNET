from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AIPinForApprovalWizard(models.TransientModel):
    _name = 'stock.inventory.approval'

    pin = fields.Char(string="PIN")
    stock_inventory_id = fields.Many2one('stock.inventory', string="Stock Inventory")

    def action_po_approve(self):
        if not self.pin:
            raise UserError(_("Favor Ingresar PIN antes de Aprobar"))

        employee = self.env.user.employee_id
        if not employee:
            raise UserError(_("Favor contactar a adminstración para que vincule su usuario a un perfil de empleado."))

        if self.pin != employee.pin:
            raise UserError(_("PIN INCORRECTO!"))
        else:
            si = self.stock_inventory_id
            si.state = "confirm"
            si.action_validate()







