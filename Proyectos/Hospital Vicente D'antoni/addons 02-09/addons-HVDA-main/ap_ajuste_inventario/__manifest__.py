{
    'name': "Aprobación: Ajuste de Inventario",
    'summary': "Aprobación con PIN para ajustes de inventario en base a Grupo de usuario.",
    'description': "Aprobación con PIN para ajustes de inventario en base a Grupo de usuario.",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'Inventory',
    'version': '0.1',
    'depends': ['base', 'stock', 'menu_aprobaciones'],
    'qweb': ['static/src/xml/validate_inventory_btn_inherit.xml'],
    'data': [
        'data/approve_mail_template.xml',
        'security/ap_ajuste_Inventario_security.xml',
        'security/ir.model.access.csv',
        'wizard/pin_for_approval_wizard_view.xml',
        'views/stock_inventory_inherit.xml',
        'views/res_company_inherit.xml',
    ],

}
