# -*- coding: utf-8 -*-
{
    'name': 'Cerrar orden de venta para pacientes internos',
    'description': 'Ocultar el botón "Editar" para cerrar orden de venta de pacientes internos',
    'author': 'HNET',
    'website': 'http://www.hnetw.com',
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale'],
    'data': [
        'views/sale_views_inherit.xml'
    ],
    'installable': True,
    'application': True,
}
