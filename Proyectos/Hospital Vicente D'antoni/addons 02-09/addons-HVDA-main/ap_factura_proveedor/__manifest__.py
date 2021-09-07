{
    'name': "PIN Aprobar Factura Proveedor",
    'summary': "Requerir pin para confirmar factura directa de proveedor",
    'description': "Requerir pin para confirmar factura directa de proveedor",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'Contabilidad',
    'version': '0.1',
    'depends': ['base', 'account', 'purchase', 'invoice_with_stock_move'],
    'data': [
        'security/ap_factura_proveedor_security.xml',
        'security/ir.model.access.csv',
        'wizard/pin_for_approval_wizard_view.xml',
        'views/account_move_view.xml',
    ]
}

