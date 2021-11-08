# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class extend_debugger(models.Model):
#     _name = 'extend_debugger.extend_debugger'
#     _description = 'extend_debugger.extend_debugger'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
