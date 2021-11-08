# -*- coding: utf-8 -*-
{
    'name': "Secuencia_Para_Clientes",

    'summary': "Al crear un nuevo contacto se asigna un correlativo de una secuencia en el campo de referencia "
               "interna para facilidad en el manejo del cliente diferenciando si es cliente normal o proveedor",

    'description': "Al crear un nuevo contacto se asigna un correlativo de una secuencia en el campo de referencia "
               "interna para facilidad en el manejo del cliente diferenciando si es cliente normal o proveedor",

    'author': "Jose Reyes",
    'category': 'Contactos',
    'version': '0.2',
    'depends': ['base'],
    'data': ['data/secuencias.xml', 'views/views.xml']
}
