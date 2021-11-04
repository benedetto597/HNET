# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 03/11/2021
    @decription Calculo de la comisión global por factura
    @name_file account_move_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""

from odoo import _, api, exceptions, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    commission_total_global = fields.Float(
        string="Comisión Global", compute="_compute_commission_total_global", store=True, readonly=True,
    )

    commission_total_salesman = fields.Float(
        string="Comisión Global Vendedor", default=0.00, store=True, readonly=True,
    )

    commission_total_manager = fields.Float(
        string="Comisión Global Gerente", default=0.00, store=True, readonly=True,
    )

    @api.depends("state")
    def _compute_commission_total_global(self):
        for record in self:

            record.commission_total_global = 0.0
            sale_order = self.env['sale.order'].search([('name', '=', record.invoice_origin)])

            # Variables necesarias
            agent = record.env['res.users'].browse(record.invoice_user_id.id)
            order_line_ids = []
        
            # Obtener los costos_id":
            for line in record.invoice_line_ids:
                order_line_ids.append(line.id)

            record.commission_total_global = sale_order.commission_total_global 
            record.commission_total_manager = sale_order.commission_total_manager 
            record.commission_total_salesman = sale_order.commission_total_salesman 
            """
            # Calcular la comisión global del agente 
            if record.amount_untaxed > 0:
                margin_percent = 35.5
                commission = agent.partner_id.commission_id
                for percents in commission.section_ids:
                    if margin_percent > percents.amount_from and  margin_percent < percents.amount_to:
                        commission_percent = percents.percent
                        
                        # Asignar la comisión al vendedor
                        record.commission_total_salesman = record.amount_untaxed * (commission_percent/100)
                        
                        # Asignar comisión adicional por gerencia
                        manager = self.env['res.partner'].search([('manager', '=', True)])
                        if len(manager) > 0 and manager.id != agent.partner_id.id:
                            commission_manager = self.env['sale.commission'].search([('manager', '=', True)])
                            if len(commission_manager) > 0:
                                for percents in commission_manager.section_ids:
                                    if margin_percent > percents.amount_from and  margin_percent < percents.amount_to:
                                        commission_percent = percents.percent 

                                        record.commission_total_manager = record.amount_untaxed * (commission_percent/100)

                        # Asignar la comisión global
                        record.commission_total_global = record.commission_total_salesman
                        if record.commission_total_manager > 0.00:
                            record.commission_total_global += record.commission_total_manager
                """
            # Establecer la comision al agente 
            agent_commissions = self.env['account.invoice.line.agent'].search([('invoice_id', '=', record.id)])
            if len(agent_commissions) >0:

                # Establecer la comision al gerente
                manager = self.env['res.partner'].search([('manager', '=', True)])
                if len(manager) > 0 and record.commission_total_manager:
                    manager_com_exist = False
                    for idx, line in enumerate(agent_commissions):
                        if line.agent_id.id == manager.id:
                            # Actualizar la comision del gerente y la de salesman
                            agent_commissions[:].amount = 0.00
                            n_idx = idx-1
                            agent_commissions[n_idx].amount = record.commission_total_salesman
                            agent_commissions[idx].amount = record.commission_total_manager
                            manager_com_exist = True
                    
                    # Crear la comision del gerente sino existe
                    if not manager_com_exist:
                        commission_manager = self.env['sale.commission'].search([('manager', '=', True)])
                        if len(commission_manager) > 0:       
                            # Agregar la comision del gerente y actualizar la de salesman
                            manager_commission = self.env['sale.order.line.agent'].create({
                                'object_id': order_line_ids[-1],
                                'agent_id': manager.id,
                                'commission_id': commission_manager.id,
                                'amount': record.commission_total_manager
                            })
                            agent_commissions[:].amount = 0.00
                            agent_commissions[-1].amount = record.commission_total_manager
                            if len(agent_commissions) > 1:                            
                                agent_commissions[-2].amount = record.commission_total_salesman
                
                else:
                    agent_commissions[:].amount = 0.00
                    agent_commissions[-1].amount = record.commission_total_global