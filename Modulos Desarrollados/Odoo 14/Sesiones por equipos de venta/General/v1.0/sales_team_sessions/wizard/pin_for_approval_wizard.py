# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Aprobación por PIN para iniciar sesión con equipo de ventas
    @name_file pin_for_approval_wizard.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class PinSalesTeamSession(models.TransientModel):
    _name = 'salesteam.sessions.approval'

    pin = fields.Char(string="PIN")
    sales_team_id = fields.Many2one('crm.team', string="Equipo de ventas")
    sale_users = fields.Many2one('hr.employee', string='Seleccione usuario')

    """ Selection Dinamico reemplazado por sale_users Many2one 
    @api.model
    def _get_sales_team_users(self):
        
            # Si no hay un id activo significa que se esta ingresando al menuite 'Sesiones de venta'

            # Obtener los usuarios incluidos en el equipo de venta al cual se quiere acceder a su sesión de ventas 
            # Obtener los usuarios para filtrar las sesiones de venta  
        
        if not self._context.get('active_id'):
            existing_users = self.env['res.users'].search([('sale_team_id', '>=', 1)])
        else:            
            existing_users = self.env['res.users'].search([('sale_team_id', '=', self._context.get('active_id'))])

        available_users = []
        for user in existing_users:
            employee = self.env['hr.employee'].search([('user_id', '=', user.id)])
            if employee:
                available_users.append(user)

        lst = []
        for user in available_users:
            lst.append((user.id, user.name))
        return lst

    # sale_users = fields.Selection(selection='_get_sales_team_users', string='Seleccione usuario')
    """

    def action_user_approve(self):
        """ 
            Crear el salesteam_config si el equipo de venta no posee uno, para poder 
                tener sesiones de venta
        
            Corroborar el PIN del usuario que del equipo de ventas y enviarlo a la vista formulario
        """
        

        selected_employee = self.sale_users
        selected_user = self.env['res.users'].browse(selected_employee.user_id).id
        if not selected_employee:
            raise UserError(_("Debe Seleccionar un Usuario"))
        else:
            if not self.pin:
                raise UserError(_("Debe Ingresar el PIN del usuario"))

            # ------- Cuando se usa el select dinamico es necesario -------
            # Empleado con PIN (El usuario no tiene PIN)
            # current_employee = self.env['hr.employee'].search([('user_id', '=', int(selected_user))])
            # Id del empleado a partir del usuario -->  print(current_employee.id)
            
            if self.pin != selected_employee.pin:
                raise UserError(_("PIN INCORRECTO!"))
            else:
                # Crear el salesteam_config sino existe
                # Id de equipo de ventas --> print(self._context.get('active_id'))
                current_crm_team_id = self._context.get('active_id')
                salesteam_config = self.env['salesteam.config'].search([('crm_team_id', '=', current_crm_team_id)])
                if not salesteam_config:
                    current_crm_team_name = self.env['crm.team'].search([('id', '=', current_crm_team_id)]).name
                    self.env['salesteam.config'].create({
                        'name': current_crm_team_name,
                        'cash_control': True,
                        'crm_team_id': current_crm_team_id,
                    })

                salesteam_config = self.env['salesteam.config'].search([('crm_team_id', '=', current_crm_team_id)])

                salesteam_session = self.env['salesteam.session'].search([('config_id', '=', salesteam_config.id)], order='id desc', limit=1)

                # Abrir sesión de ventas
                if not salesteam_session or salesteam_session.state == 'closed':
                    salesteam_config.open_session_cb(current_crm_team_id, selected_employee.user_id.id)
                    salesteam_session = self.env['salesteam.session'].search([('config_id', '=', salesteam_config.id)], order='id desc', limit=1)
                    salesteam_session._get_current_user(selected_user) 

                # Continuar sesión de ventas
                else:
                    salesteam_session._get_current_user(selected_user) 
                    salesteam_config.open_existing_session_cb()

                    # Aumentar el login_number por el usuario loggeandose correctamente
                    salesteam_session.login()

                # Direccionar a la vista form de la sesión de ventas
                domain = []
                res_id = salesteam_session.id
                search_action = self.env.ref('sales_team_sessions.action_sales_team_session_form').read()[0]
                res = dict(search_action, domain=domain, res_id=res_id)
                return res
