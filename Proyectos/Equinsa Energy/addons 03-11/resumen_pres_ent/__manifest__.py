{
    'name': "Resumen Costo entregadas vs presupuestadas",
    'summary': "Resumen Costo entregadas vs presupuestadas",
    'description': "Resumen Costo entregadas vs presupuestadas",
    'author': "HNET",
    'website': "http://www.hnetw.com",
    'category': 'Sales',
    'version': '13.0.1',
    'depends': ['base', 'sale', 'project', 'sale_margin', 'stock', 'cc_cotizaciones'],
    'data': [
        'security/ir.model.access.csv',
        'views/resumen_transferencias_view.xml',
        'views/project_project_views.xml',
        'views/razon_desviacion_view.xml',
    ],
}
