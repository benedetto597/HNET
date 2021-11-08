# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------
    
    @author ebenedetto@hnetw.com - HNET
    @date 27/07/2021
    @decription Datos de la factura personalizada (CAI - ISV's)
    @name_file pos_ticket_custom.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models, tools, _


class pos_order(models.Model):
    """
    Definir número de facturación (Secuencia POS_CAI)
    Datos del cliente exonerado
    Desgloce de impuestos para la factura
    """
    _inherit = 'pos.order'

    facturacion = fields.Char("N° de Facturación")

    note1 = fields.Text("N° O/C Excenta")
    note2 = fields.Text("N° Registro Exonerado")
    note3 = fields.Text("N° Registeo SAG")
    is_tax_free_order = fields.Boolean("Is Tax free order?", default=False)
    exento = fields.Char("Impuesto Exento")

    tax_15 = fields.Float(string="ISV 15%")
    tax_18 = fields.Float(string="ISV 18%")
    tax_bf1 = fields.Float(string="Base Exento")
    tax_bf2 = fields.Float(string="Base 15%")
    tax_bf3 = fields.Float(string="Base 18%")

    @api.model
    def _amount_line_tax_new(self, line, tax_name):
        
        taxes_ids = line.product_id.taxes_id

        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        taxes = taxes_ids.compute_all(price, None, line.qty, product=line.product_id.id,
                                      partner=line.order_id.partner_id or False)['taxes']
        val = 0.0
        for c in taxes:
            if c.get('name', '') == tax_name:
                val += c.get('amount', 0.0)
        return val

    @api.model
    def _amount_line_tax_new2(self, line, tax_name):
        # taxes_ids = [tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id]
        # print("Testing the objects>>>>>>>>>>>>>>>>>>>>>>>>>1212",taxes_ids)
        # taxes_obj_ids = self.env['account.tax'].sudo().search([('id','in',taxes_ids)])
        # print("Testing the objects>>>>>>>>>>>>>>>>>>>>>>>>>",taxes_obj_ids)
        taxes_ids = line.product_id.taxes_id

        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        taxes = taxes_ids.compute_all(price, None, line.qty, product=line.product_id.id,
                                      partner=line.order_id.partner_id or False)['taxes']
        val = 0.0
        for c in taxes:
            if c.get('name', '') == tax_name:
                val += line.price_subtotal
                break
        return val

    def _calculate_base(self, order):
        result = {}

        base_15 = 0
        tax_15 = 0
        base_18 = 0
        base_exento = 0
        tax_18 = 0

        for line in order.lines:
            tax_15 += self._amount_line_tax_new(line, "15% ISV")
            tax_18 += self._amount_line_tax_new(line, "18% ISV")
            base_15 += self._amount_line_tax_new2(line, "15% ISV")
            base_18 += self._amount_line_tax_new2(line, "18% ISV")
            base_exento += self._amount_line_tax_new2(line, "Exento")

        result['tax_15'] = tax_15
        result['tax_18'] = tax_18
        result['tax_bf1'] = base_exento
        result['tax_bf2'] = base_15
        result['tax_bf3'] = base_18

        return result

    @api.model
    def create(self, values):
        order = super(pos_order, self).create(values)
        seq = order.session_id.config_id.pos_order_secuencia_id
        if seq and values.get("amount_paid") >= 1:
            name = seq.next_by_id()
            _taxes = self._calculate_base(order)
            for key, value in _taxes.items():
                order.write({key: value})
            order.write({'facturacion': name})
        print(order.tax_15)
        return order

    # Necesario para la comunicación entre el backend y frontend
    def _export_for_ui(self, order):
        return {
            'tax_15' : order.tax_15,
            'tax_18' : order.tax_18,
            'tax_bf1' : order.tax_bf1,
            'tax_bf2' : order.tax_bf2,
            'tax_bf3' : order.tax_bf3,
            'note1': order.note1,
            'note2': order.note2,
            'note3': order.note3,
            'facturacion': order.facturacion,
            'exento': order.exento,
        }

    def export_for_ui(self):
        return self.mapped(self._export_for_ui) if self else []

"""
    @api.model
    def correr_num_factura(self, seq_id):

        seq = self.env['ir.sequence'].sudo().search([('id', '=', seq_id)])
        if seq:
            name = seq.next_by_id()
            return name
        return False

    def _order_fields(self, ui_order):
        session = self.env["pos.session"].search([("id", "=", ui_order.get("pos_session_id"))])
        seq = session.config_id.pos_order_secuencia_id
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