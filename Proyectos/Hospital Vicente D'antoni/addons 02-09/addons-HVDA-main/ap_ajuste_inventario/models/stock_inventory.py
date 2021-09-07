from odoo import models, fields, api, _


EXTRA_STATUS = [('to_approve', 'Para Aprobar')]


class StockInventoryInherit(models.Model):
    _inherit = 'stock.inventory'

    state = fields.Selection(selection_add=EXTRA_STATUS, string='Status')

    def request_approval(self):
        self.state = 'to_approve'
        self.send_email_next()

    def action_validate_pin(self):
        return self.get_pin_wiz()

    def send_email_next(self):
        user_group = self.env.ref("ap_ajuste_inventario.ap_ajuste_inventario")
        users_emails = self.get_email_to(user_group)
        approv_template_id = self._get_email_template_id()
        ctx = self._context.copy()
        ctx.update({'email_to': users_emails})
        if approv_template_id:
            approv_template_id.with_context(ctx).send_mail(self.id)
        return True

    def get_email_to(self, user_group):
        email_list = [
            usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        return ",".join(email_list)

    def _get_email_template_id(self):
        return self.env.user.company_id.ai_email_tmpl_id

    def get_pin_wiz(self):
        wizard_form = self.env.ref('ap_ajuste_inventario.pin_for_approval_ai_form', False)
        wiz_model_id = self.env['stock.inventory.approval']
        vals = {
            'stock_inventory_id': self.id,
        }
        new = wiz_model_id.create(vals)

        return {
            'name': _('Aprobación Ajuste Inventario'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inventory.approval',
            'res_id': new.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }
