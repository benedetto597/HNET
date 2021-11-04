# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    actual_qty_available = fields.Float(
        'Actual Quantity', compute='_compute_actual_quantities',
        compute_sudo=False, digits='Product Unit of Measure')

    @api.depends('qty_available', 'virtual_available')
    def _compute_actual_quantities(self):
        for product in self:
            product.actual_qty_available = product.qty_available - product.outgoing_qty


class ProductProduct(models.Model):
    _inherit = 'product.product'

    actual_qty_available = fields.Float(
        'Actual Quantity', compute='_compute_actual_quantities',
        compute_sudo=False, digits='Product Unit of Measure')

    @api.depends('qty_available', 'virtual_available')
    def _compute_actual_quantities(self):
        for product in self:
            product.actual_qty_available = product.qty_available - product.outgoing_qty
