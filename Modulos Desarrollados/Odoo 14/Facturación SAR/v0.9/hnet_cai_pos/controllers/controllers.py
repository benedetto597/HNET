# -*- coding: utf-8 -*-
# from odoo import http


# class HnetCaiPos(http.Controller):
#     @http.route('/hnet_cai_pos/hnet_cai_pos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hnet_cai_pos/hnet_cai_pos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hnet_cai_pos.listing', {
#             'root': '/hnet_cai_pos/hnet_cai_pos',
#             'objects': http.request.env['hnet_cai_pos.hnet_cai_pos'].search([]),
#         })

#     @http.route('/hnet_cai_pos/hnet_cai_pos/objects/<model("hnet_cai_pos.hnet_cai_pos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hnet_cai_pos.object', {
#             'object': obj
#         })
