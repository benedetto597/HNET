# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class pos_config(models.Model):
    _inherit = 'pos.config'

    pos_order_sequence_prefix = fields.Char('Pos order sequence prefix')
    pos_order_sequence_id = fields.Many2one('ir.sequence', 'Pos order sequence')

    @api.model
    def _update_pos_order_sequence_id(self, values):
        prefix = values.get('pos_order_sequence_prefix')
        if not prefix:
            return values
        seq_id = values.get('pos_order_sequence_id')
        if not seq_id:
            seq_id = self.env['ir.sequence'].create({
                'name':'Pos order sequence',
                'padding':8,
                'code':'pos.order.custom',
                'prefix': prefix,
                'active' : True,
                })
            values.update({'pos_order_sequence_id':seq_id})
        else:
            seq_obj = self.env['ir.sequence'].browse(seq_id)
            seq_obj.write({
                'prefix': prefix
            })
        return values

    @api.model
    def create(self,values):
        self._update_pos_order_sequence_id(values)
        return super(pos_config, self).create(values)

    def write(self, vals):
        values = {}
        for conf in self:
            values = vals.copy()
            if conf.pos_order_sequence_id:
                values.update({'pos_order_sequence_id': conf.pos_order_sequence_id.id})
            self._update_pos_order_sequence_id(values)
        return super(pos_config, self).write(values)

class pos_order(models.Model):
    _inherit = 'pos.order'

    facturacion = fields.Char("N° de Facturación")
    note1 = fields.Text("N° O/C Exenta")
    note2 = fields.Text("N° Registro Exonerado")
    note3 = fields.Text("N° Registeo SAG")
    is_tax_free_order = fields.Boolean("Is Tax free order?", default=False)
    exento = fields.Char("Impuesto Exento")

    @api.model
    def correr_num_factura(self, seq_id):

        seq = self.env['ir.sequence'].sudo().search([('id', '=', seq_id)])
        if seq:
            name = seq.next_by_id()
            return name
        return False

    @api.model
    def create(self, values):
        order = super(pos_order, self).create(values)
        """
        seq = order.session_id.config_id.pos_order_sequence_id
        if seq and values.get("amount_paid") >=1:
            name = seq.next_by_id()
            order.write({'facturacion': name})
        """
        print(order)
        return order
"""
    @api.model
    def _order_fields(self, ui_order):
        session = self.env["pos.session"].search([("id", "=", ui_order.get("pos_session_id"))])
        seq = session.config_id.pos_order_sequence_id
        if seq and ui_order.get("amount_paid") >= 1 and ui_order.get("facturacion"):
            seq.next_by_id()

        res = super(pos_order, self)._order_fields(ui_order)
        res['note1'] = ui_order['note1']
        res['note2'] = ui_order['note2']
        res['note3'] = ui_order['note3']
        res['facturacion'] = ui_order['facturacion']
        res['exento'] = ui_order['exento']
        return res
"""