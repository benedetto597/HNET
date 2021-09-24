# -*- coding: utf-8 -*-
{
    'name': "CAI POS",
    'summary': "Facturacion del SAR Odoo14",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'POS',
    'version': '1.0',
    'depends': ['base', 'point_of_sale'],
    'qweb': [
        'static/src/xml/pos.xml',
        'static/src/xml/datos_sar.xml',
             ],
    'data': [
        'views/cai_pos_templates.xml',
        'views/pos_cai_views.xml',
    ],
}
