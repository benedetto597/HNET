# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicianSpecialty(models.Model):
    _name = 'physician.specialty'
    _description = "Physician Specialty"

    code = fields.Char(string='Code')
    name = fields.Char(string='Specialty', required=True, translate=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class PhysicianDegree(models.Model):
    _name = 'physician.degree'
    _description = "Physician Degree"

    name = fields.Char(string='Degree')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class Physician(models.Model):
    _inherit = 'hms.physician'

    employee_id = fields.Many2one('hr.employee',string='Empleado', required=True,
        ondelete='cascade', help='Employee-related data of the physician')

    @api.model
    def create(self, values):
        vals = super(Physician, self).create(values)

        employee_id = self.env['hr.employee'].create({
            'name': values['name'],
            'user_id': vals.user_id.id,
            'address_home_id': vals.user_id.partner_id.id,
            'address_id': vals.user_id.partner_id.id,
            'company_id': values['company_id'],
            'work_phone': values['phone'],
            'mobile_phone': values['mobile'],
            'work_email': values['email'],
        })

        self.employee_id = employee_id.id

        return vals

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
# {'image_1920': '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', 
# '__last_update': False, 
# 'name': 'asfssf', 
# 'degree_ids': [[6, False, [1]]], 
# 'medical_license': 'fsafdasdas', 
# 'user_id': False, 
# 'consultaion_service_id': 41, 
# 'followup_service_id': 2, 
# 'appointment_duration': 0.25, 
# 'is_primary_surgeon': False, 
# 'company_id': 1, 
# 'specialty_id': 1, 
# 'department_ids': [[6, False, [1]]], 
# 'type': 'contact', 
# 'parent_id': False, 
# 'street': 'fasfasassss', 
# 'street2': 'fasfa', 
# 'city': 'fasfa', 
# 'state_id': 248, 
# 'zip': '425245', 
# 'country_id': 3, 
# 'website': 'dsadsa', 
# 'phone': '2444424', 
# 'mobile': '45524245', 
# 'user_ids': [], 'email': 
# 'adsdsa@mail.com', 
# 'signature': False, 
# 'message_follower_ids': [], 
# 'activity_ids': [], 
# 'message_ids': [], 
# 'code': 'DR014', 
# 'login': 'adsdsa@mail.com'}
