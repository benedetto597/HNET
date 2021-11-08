# -*- coding: utf-8 -*-

import base64

from odoo import http,tools, _
from odoo.http import request
from odoo.addons.im_livechat.controllers.main import LivechatController


class LivechatControllerInherit(LivechatController):

    @http.route('/im_livechat/load_templates', type='json', auth='none', cors="*")
    def load_templates(self, **kwargs):
        base_url = request.httprequest.base_url
        templates = [
            'short_name_operator_livechat/static/src/legacy/public_livechat.xml',
        ]
        return [tools.file_open(tmpl, 'rb').read() for tmpl in templates]