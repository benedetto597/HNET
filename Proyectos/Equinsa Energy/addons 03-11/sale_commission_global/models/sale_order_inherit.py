# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 03/11/2021
    @decription Calculo de la comisión global por orden de venta
    @name_file sale_order_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("amount_untaxed", "invoice_status")
    def _compute_commission_total_global(self):
        """ Calcular la comisión global
        --> Sumando los gastos por producto
        --> Restando de la base imponible los gastos sumados
        R// Margen de ganancia
        --> Del margen de ganancia en porcentaje obtener
        --> El porcentaje a de la base imponible que le será de comisión al agente
        --> Si el agente no es gerente se le debe agregar también la comisión del gerente
        R// Comisión global, de agente y de gerente
        """

        for order in self:
            # Variables necesarias
            agent = order.env['res.users'].browse(order.user_id.id)
            order_line_ids = []
            
            # Obtener las lineas de pedido
            for line in order.order_line:
                order_line_ids.append(line.id)

            # Calcular la comisión global del agente 
            if order.amount_untaxed > 0:
                margin_percent = order.margen_porcentaje
                commission = agent.partner_id.commission_id
                for percents in commission.section_ids:
                    if margin_percent > percents.amount_from and margin_percent < percents.amount_to:
                        commission_percent = percents.percent

                        # Asignar la comisión al vendedor
                        order.commission_total_salesman = order.amount_untaxed * (commission_percent/100)
                        
                        # Asignar comisión adicional por gerencia
                        manager = self.env['res.partner'].search([('manager', '=', True)])
                        if len(manager) > 0 and manager.id != agent.partner_id.id:
                            commission_manager = self.env['sale.commission'].search([('manager', '=', True)])
                            if len(commission_manager) > 0:
                                for percents in commission_manager.section_ids:
                                    if margin_percent > percents.amount_from and  margin_percent < percents.amount_to:
                                        commission_percent = percents.percent 

                                        order.commission_total_manager = order.amount_untaxed * (commission_percent/100)

                # Asignar la comisión global
                order.commission_total_global = order.commission_total_salesman
                if order.commission_total_manager > 0.00:
                    order.commission_total_global += order.commission_total_manager

            # Establecer la comision al agente 
            agent_commissions = self.env['sale.order.line.agent'].search([('object_id', 'in', order_line_ids)])
            if len(agent_commissions) >0:

                # Establecer la comision al gerente
                manager = self.env['res.partner'].search([('manager', '=', True)])
                if len(manager) > 0 and order.commission_total_manager:
                    manager_com_exist = False
                    for idx, line in enumerate(agent_commissions):
                        if line.agent_id.id == manager.id:
                            # Actualizar la comision del gerente y la de salesman
                            agent_commissions[:].amount = 0.00
                            n_idx = idx-1
                            agent_commissions[n_idx].amount = order.commission_total_salesman
                            agent_commissions[idx].amount = order.commission_total_manager
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
                                'amount': order.commission_total_manager
                            })
                            agent_commissions[:].amount = 0.00
                            agent_commissions[-1].amount = order.commission_total_manager
                            if len(agent_commissions) > 1:                            
                                agent_commissions[-2].amount = order.commission_total_salesman
                else:
                    agent_commissions[:].amount = 0.00
                    agent_commissions[-1].amount = order.commission_total_global

    commission_total_global = fields.Float(
        string="Comisión Global", compute="_compute_commission_total_global", store=True, readonly=True,
    )

    commission_total_salesman = fields.Float(
        string="Comisión Global Vendedor", default=0.00, store=True, readonly=True,
    )

    commission_total_manager = fields.Float(
        string="Comisión Global Gerente", default=0.00, store=True, readonly=True,
    )
