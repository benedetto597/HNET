from odoo import fields, models, _


class PurchaseOrderRefuseWizard(models.TransientModel):
    _name = 'purchase.order.refuse.wizard'

    note = fields.Text(
        string="Motivo de Rechazo",
        required=True,
    )

    def action_po_refuse(self):
        purchase_order_id = self.env['purchase.order'].browse(int(self._context.get('active_id')))
        for rec in self:
            purchase_order_id.refuse_reason_note = rec.note
            purchase_order_id.po_refuse_user_id = rec.env.uid
            purchase_order_id.po_refuse_date = fields.date.today()
            refuse_template_id = purchase_order_id._get_refuse_template_id()
            ctx = self._context.copy()

            ctx.update({
                'name': purchase_order_id.create_uid.partner_id.name,
                'email_to': purchase_order_id.create_uid.partner_id.email,
                'subject': _('Orden de Compra: ') + purchase_order_id.name + _(' Rechazada'),
                'manager_name': rec.env.user.name,
                'reason': rec.note,
                })

            if refuse_template_id:
                refuse_template_id.with_context(ctx).send_mail(purchase_order_id.id)

            purchase_order_id.state = 'refuse'

