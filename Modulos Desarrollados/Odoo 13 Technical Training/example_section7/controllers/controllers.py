# -*- coding: utf-8 -*-
from odoo import http


class MyFirstModule(http.Controller):
    @http.route('/example_section7/example_section7/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/example_section7/example_section7/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('example_section7.listing', {
            'root': '/example_section7/example_section7',
            'objects': http.request.env['example_section7.example_section7'].search([]),
        })

    @http.route('/example_section7/example_section7/objects/<model("example_section7.example_section7"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('example_section7.object', {
            'object': obj
        })
