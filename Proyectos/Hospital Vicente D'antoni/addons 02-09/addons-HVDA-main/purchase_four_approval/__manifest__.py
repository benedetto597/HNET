# -*- coding: utf-8 -*-
{

    'name': 'Purchase Four Approval',
    'version': '1.2.1',
    'category': 'Purchases',
    'summary': 'Agregar cuatro niveles de aprobación a la compra',
    'description': 'Agregar cuatro niveles de aprobación a la compra',
    'depends': ['purchase'],
    'data': [
            'data/approve_mail_template.xml',
            'data/refuse_mail_template.xml',
            'security/purchase_security.xml',
            'security/ir.model.access.csv',
            'wizard/pin_for_approval_wizard_view.xml',
            'wizard/purchase_order_refuse_wizard_view.xml',
            'views/purchase_view.xml',
            'views/res_company_view.xml',
             ],
    'installable': True,
}
