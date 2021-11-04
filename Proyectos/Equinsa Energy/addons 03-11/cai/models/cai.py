# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning


class fiscal_regimen(models.Model):
    _name = "dei.fiscal_regime"

    cai = fields.Many2one('dei.cai', required=True)
    sequence = fields.Many2one('ir.sequence', string="Sequencia")
    selected = fields.Boolean('selected')
    desde = fields.Integer('Desde')
    hasta = fields.Integer('A')

    para_facturacion = fields.Boolean("Secuencia para Facturacion")


@api.constrains
def dei_validate(self):
    if self.dei.fiscal_regime:
        if self.desde > self.hasta:
            raise Warning('lXXXX')


@api.onchange('selected')
def disable_other_regimes(self):
    if self.selected:
        lista = self.env['dei.fiscal_regime'].search([('sequence.name', '=', self.sequence.name)])
        lista.write({'selected': 0})
        self.write({'selected': 1})


class cai(models.Model):
    _name = "dei.cai"
    name = fields.Char('CAI', help='Clave de Autorización de Impresion ', required=True, select=True)
    expiration_date = fields.Date('Fecha Limite de Impresion', required=True, select=True)
    company = fields.Many2one('res.company', string="Compañia", required=True)
    fiscal_regimes = fields.One2many('dei.fiscal_regime', 'cai')

    tipo_cai = fields.Selection([
        ("out_invoice", "facturación"),
        ("out_refund", "Nota de Crédito")
    ])

    @api.constrains('expiration_date')
    def check_unique_default_date(self):
        for obj in self:
            if obj.expiration_date < fields.Date.today():
                raise Warning("La fecha no puede ser  menor .")
