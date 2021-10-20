# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 19/10/2021
    @decription Mostrar solamente el nombre de pila en la nav bar del Live Chat
    @name_file im_livechat_inherit.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import api, fields, models

class ImLivechatChannelInherit(models.Model):
    _inherit = 'im_livechat.channel'

    def _get_livechat_mail_channel_vals(self, anonymous_name, operator, user_id=None, country_id=None):
        #res = super(ImLivechatChannelInherit, self). _get_livechat_mail_channel_vals(self, anonymous_name, operator, user_id, country_id)
        operator_partner_id = operator.partner_id.id
        channel_partner_to_add = [(4, operator_partner_id)]
        visitor_user = False
        if user_id:
            visitor_user = self.env['res.users'].browse(user_id)
            if visitor_user and visitor_user.active:  # valid session user (not public)
                channel_partner_to_add.append((4, visitor_user.partner_id.id))

        return {
            'channel_partner_ids': channel_partner_to_add,
            'livechat_active': True,
            'livechat_operator_id': operator_partner_id,
            'livechat_channel_id': self.id,
            'anonymous_name': False if user_id else anonymous_name,
            'country_id': country_id,
            'channel_type': 'livechat',
            'name': ' - '.join([visitor_user.display_name if visitor_user else anonymous_name, ((operator.livechat_username).split(' '))[0] if operator.livechat_username else ((operator.name).split(' '))[0]]),
            'public': 'private',
            'email_send': False,
        }