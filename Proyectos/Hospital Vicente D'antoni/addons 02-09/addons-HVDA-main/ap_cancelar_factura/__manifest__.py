{
    'name': "PIN Cancelar Factura",
    'summary': "Requerir pin para eliminar Factura",
    'description': "Requerir pin para eliminar Factura",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'Contabilidad',
    'version': '0.1',
    'depends': ['base', 'account'],
    'data': [
        'security/ap_cancelar_factura_security.xml',
        'security/ir.model.access.csv',
        'wizard/pin_for_approval_wizard_view.xml',
        'views/account_move_view.xml',
    ]
}

