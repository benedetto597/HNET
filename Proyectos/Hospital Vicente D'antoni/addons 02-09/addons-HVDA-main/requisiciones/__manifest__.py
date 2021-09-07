# -*- coding: utf-8 -*-
{
    'name': "Requisiciones",
    'summary': "Modelo para el manejo de Requisiciones del hospital Vicente D' Antoni",
    'description': "Modelo para el manejo de Requisiciones del hospital Vicente D' Antoni",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'Requisiciones',
    'version': '0.1',
    'depends': ['base', 'purchase', 'product'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/requisicion.xml',
        'views/requisicion_condensada.xml',
        'views/requisicion_linea.xml',
        'views/stock_location_inherit.xml',
        'views/product.xml',
    ],
    'application': True,
}
