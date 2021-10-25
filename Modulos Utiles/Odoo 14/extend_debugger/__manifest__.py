
from . import models{
    'name': "Extend Debugger Menu",
    'summary': "Add view, models and actions menu from technical to odoo debug menu",
    'description': "Add view, models and actions menu from technical to odoo debug menu",
    'author': "Jose Reyes",
    'category': 'Technical',
    'version': '0.1',
    'depends': ['base', 'base_automation'],
    'qweb': [
        'static/src/xml/inherit_btn_view.xml'
    ],
    'data': [
        'views/assets.xml',
    ],
}
