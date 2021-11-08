{
    'name': "Campos Calculados en Cotizaciones",
    'summary': "Campos Calculados en Cotizaciones solicitados por EQUINSA",
    'description': "Campos Calculados en Cotizaciones solicitados por EQUINSA",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'Sale',
    'version': '13.0.1',
    'depends': ['base', 'sale', 'sale_commission', 'sale_margin'],
    'data': [
        'views/views.xml',
        'security/sale_cc_security.xml',
        'views/res_config_settings_view.xml',
    ],
}
