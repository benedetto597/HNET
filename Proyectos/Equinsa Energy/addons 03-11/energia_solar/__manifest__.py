# -*- coding: utf-8 -*-
{
    'name': "energia_solar",
    'summary': "Agregar calculos extra en subscripcion",
    'description': "Agregar calculos extra en subscripcion",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'subscription',
    'version': '1.0',
    'depends': ['base', 'sale_subscription', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_table_entry.xml',
        'data/secuencia.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
}
