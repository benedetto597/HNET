# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 19/10/2021
    @decription Mostrar solamente el nombre de pila en el contenido del Live Chat
    @name_file res_partner_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models

class PartnersInherit(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        if self.env.context.get('im_livechat_use_username'):
            # process the ones with livechat username
            users_with_livechatname = self.env['res.users'].search([('partner_id', 'in', self.ids), ('livechat_username', '!=', False)])
            map_with_livechatname = {}
            for user in users_with_livechatname:
                map_with_livechatname[user.partner_id.id] = user.livechat_username

            # process the ones without livecaht username
            partner_without_livechatname = self - users_with_livechatname.mapped('partner_id')
            no_livechatname_name_get = super(PartnersInherit, partner_without_livechatname).name_get()
            map_without_livechatname = dict(no_livechatname_name_get)

            # restore order
            result = []
            for partner in self:
                name = map_with_livechatname.get(partner.id)
                if not name:
                    name = map_without_livechatname.get(partner.id)
                    name_split = (name.split(' '))
                    name = ' '.join([name_split[0], name_split[1]])
                result.append((partner.id, name))
        else:
            result = super(PartnersInherit, self).name_get()
            user_name = (result[0])[2]
            short_name = (user_name.split(' '))[0]
            result = [((result[0])[0], (result[0])[1]), short_name]
        return result