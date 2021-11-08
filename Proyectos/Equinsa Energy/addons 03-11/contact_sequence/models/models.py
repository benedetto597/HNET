from odoo import models, fields, api, _


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([('client', 'Client'), ('supplier', 'Supplier')], string="Contact Type")

    @api.model
    def create(self, vals):

        vals['supplier_rank'] = 1 if vals.get('contact_type') == 'supplier' else 0
        sequence_code = 'supplier.partner.sequence' if vals.get('supplier_rank') > 0 else 'client.partner.sequence'
        vals['ref'] = self.env['ir.sequence'].next_by_code(sequence_code)

        result = super(ResPartnerInherit, self).create(vals)

        return result

