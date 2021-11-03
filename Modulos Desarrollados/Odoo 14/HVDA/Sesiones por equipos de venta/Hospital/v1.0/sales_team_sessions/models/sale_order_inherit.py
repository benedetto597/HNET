# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Tipos de pago y id por sesión de equipo de ventas en orden de venta (Herencia - Orden de venta)
    @name_file sale_order_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import models,fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    """ Incluir para la version del Hospital Vicente D'antoni
    DIRECT_SALE_OPTIONS = [
        ('hospitalization', 'Hospitalización'), 
        ('external_consultation', 'Consulta Externa'),               
        ('emergency', 'Emergencia'),
    ]

    is_direct_sale = fields.Boolean(string='Has Cash Control', default=False,
        help="Definir si la orden de venta pertenece a una venta directa")

    direct_sale = fields.Selection(
        DIRECT_SALE_OPTIONS, string='Status', index=True, copy=False,
        help='Seleccion de los distintos tipos de ventas para las ventas directas')
    """ 
    payment_ids = fields.One2many('salesteam.payment', 'sale_order_id', string='Pagos', readonly=True)
    salesteam_session_id = fields.Many2one('salesteam.session', string='Sesión de equipo de ventas', store=True)
    payment_method_selected = fields.Char(string='Método de pago', compute='_compute_selected_payment_method')

    @api.depends('invoice_status')
    def _compute_selected_payment_method(self):
        for sale in self:
            sale_account_move = self.env['account.move'].search([('invoice_origin', '=', sale.name)], order='id', limit=1)
            if not sale_account_move:
                sale.payment_method_selected = 'Sin Facturar'
            else:
                sale_payment_register = self.env['account.payment.register'].search([('communication', '=', sale_account_move.name)], order='id', limit=1)
                if not sale_payment_register:
                    sale.payment_method_selected = 'Sin Pagar'
                else:
                    sale.payment_method_selected = sale_payment_register.payment_method_selection
                    
    @api.model
    def create(self, vals):
        """ 
            Overwrite 

            Si el equipo de venta que se coloque en la orden de venta tiene una 
                sesión de venta abierta se coloca el id en salesteam_session_id

            No se permite crear la orden de venta si el equipo de venta no 
                tiene una sesión de venta activa 
        """

        team_id = vals['team_id']
        salesteam_config = self.env['salesteam.config'].search([('crm_team_id', '=' , team_id)])
        if not salesteam_config:
            raise ValidationError(_('Debe inciar una sesión de ventas con el equipo de ventas seleccionado.'))
        
        salesteam_session = self.env['salesteam.session'].search([('config_id', '=' , salesteam_config.id)], order='id desc', limit=1)
        if not salesteam_session or salesteam_session.state != 'opened':
            raise ValidationError(_('Debe inciar una sesión de ventas con el equipo de ventas seleccionado.'))
        
        vals['salesteam_session_id'] = salesteam_session.id
            
        result = super(SaleOrder, self).create(vals)
        return result
