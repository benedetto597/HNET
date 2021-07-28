# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010-2016  HM Consulting <info@odoohonduras.com>
# (http://odoohonduras.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, tools, _

class pos_order(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def _amount_line_tax_new(self,line, tax_name):
        # taxes_ids = [tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id]
        taxes_ids = line.product_id.taxes_id

        # taxes_obj_ids = self.env['account.tax'].sudo().search([('id','in',taxes_ids)])
        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        taxes = taxes_ids.compute_all(price, None,line.qty, product=line.product_id.id, partner=line.order_id.partner_id or False)['taxes']
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
        taxes = taxes_ids.compute_all(price, None, line.qty, product=line.product_id.id, partner=line.order_id.partner_id or False)['taxes']
        val = 0.0
        for c in taxes:
            if c.get('name', '') == tax_name:
                val += line.price_subtotal
                break
        return val

    def _compute_base(self):
        result = {}
        
        for order in self:
            base_15 = 0
            tax_15 = 0
            base_18 = 0
            base_exento = 0
            tax_18 = 0

            for line in order.lines:
                print(line)
                tax_15 += self._amount_line_tax_new(line, "15% ISV")
                tax_18 += self._amount_line_tax_new(line, "18% ISV")
                base_15 += self._amount_line_tax_new2(line, "15% ISV")
                base_18 += self._amount_line_tax_new2(line, "18% ISV")
                base_exento += self._amount_line_tax_new2(line, "Exento")
        
            order.tax_15 = tax_15
            order.tax_18 = tax_18
            order.tax_bf1 = base_exento
            order.tax_bf2 = base_15
            order.tax_bf3 = base_18

    
    
    tax_15 = fields.Float(string="ISV 15%",compute='_compute_base')
    tax_18 = fields.Float(string="ISV 18%",compute='_compute_base')
    tax_bf1 = fields.Float(string="Base Exento",compute='_compute_base')
    tax_bf2 = fields.Float(string="Base 15%",compute='_compute_base')
    tax_bf3 = fields.Float(string="Base 18%",compute='_compute_base')
    

