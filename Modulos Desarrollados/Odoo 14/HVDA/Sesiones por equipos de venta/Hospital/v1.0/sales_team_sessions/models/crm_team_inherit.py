# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 22/09/2021
    @decription Registro de inicio de sesión por PIN para empleado por equipo de ventas (Herencia - CRM Team)
    @name_file crm_team_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo.exceptions import ValidationError
from odoo import models,fields, api, _

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    def pin_button_access_session(self):
        """ Llamado al wizard """
        return self.get_pin_access_session_wiz()

    def get_pin_access_session_wiz(self):
        """ 
            Llamado al wizard para seleccionar usuario de equipo de venta y colocar pin 
                para acceder a la sesión de ventas de ese equipo
        """
        wizard_form = self.env.ref('sales_team_sessions.pin_for_approval_user_form', False)
        wiz_model_id = self.env['salesteam.sessions.approval']
        # Seleccionar al usuario loggeado si se encuentra en el equipo de ventas al que pertenece
        if self.env.user.sale_team_id.id == self.id:
            employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
            vals = {
                'sales_team_id': self.id,
                'sale_users': employee_id,
            }

        else:
            vals = {
                'sales_team_id': self.id,
            }
        new = wiz_model_id.create(vals)

        return {
            'name': _('Aprobación Sesión De Ventas'),
            'type': 'ir.actions.act_window',
            'res_model': 'salesteam.sessions.approval',
            'res_id': new.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }

    def unlink(self):
        """ Eliminar la configuración de la sesión de ventas del equipo de venta """

        salesteam_config = self.env['salesteam.config'].search([('crm_team_id', '=', self.id)])
        salesteam_sessions = self.env['salesteam.session'].search([('config_id', '=', salesteam_config.id)])

        # Comprobar si existen sesiones abiertas con el equipo de venta a eliminar
        salesteam_session_opened = salesteam_sessions.filtered(lambda session: session.state != 'closed')
        if salesteam_session_opened:
            raise ValidationError(_("Debe cerrar todas las sesiones de venta del equipo de venta antes de eliminarlo"))
        
        # Desactivar la configuración de la sesión de ventas
        salesteam_config.active = False

        return super().unlink()

