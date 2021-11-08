# -*- coding: utf-8 -*-
{
    'name': 'Sesiones Equipos de Venta',
    'description': 'Sesiones de venta por equipo de venta',
    'summary': """
        
        Sesiones de venta por equipo de venta
        =============================================================================
        Inicio de sesión de ventas para cada equipo de ventas
        Inicio restringido por usuario agregado al equipo de ventas y PIN de empleado
        Control de apertura y cierre de caja
        Despliegue de sesiones de venta a partir de grupos de usuarios
        
        """,
    'author': 'HNET',
    'website': 'http://www.hnetw.com',
    'category': 'Sales/Sales',
    'version': '0.9',
    'depends': ['base', 'sale', 'sales_team', 'account'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/sales_team_sequence.xml',
        'data/sales_team_data.xml',
        'data/salesteam_session_sequence.xml',
        'views/crm_team_views.xml',
        'views/salesteam_session_views.xml',
        'views/sale_order_views_inherit.xml',
        'views/salesteam_payment_views.xml',
        'views/account_statement_view.xml',
        'views/account_payment_register_views_inherit.xml',
        'wizard/pin_for_approval_wizard_view.xml',
        'wizard/salesteam_box.xml',
    ],
    'qweb': [
        'static/src/xml/base_inherit.xml',
    ],
    'installable': True,
    'application': True,
}
