# -*- coding: utf-8 -*-
{
    'name': "Impresion de Documentos Fiscales",
    'description': """
    """,

    'author': "Tommy Ponce",
    'website': "http://www.intelsoftone.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '0.1',
    'active': False,
    'update_xml': [],

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/res_currency_data.xml',
        'views/res_currency.xml',
        'views/res_company.xml',
        'views/invoice_view.xml',
        'views/cai_view.xml',
        'views/ir_sequence_view.xml',
        'report.xml',
        'report_invoice.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'auto_install': False,
    'installable': True,
    'application': False,

}
