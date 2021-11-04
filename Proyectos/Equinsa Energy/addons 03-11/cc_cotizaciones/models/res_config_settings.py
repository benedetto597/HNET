from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    administracion = fields.Float(default=0.07, string="porcentaje Administración", config_parameter='cc_cotizaciones.administracion')
    imprevistos = fields.Float(default=0.1, string="porcentaje Imprevistos", config_parameter='cc_cotizaciones.imprevistos')
    utilidad = fields.Float(default=0.7, string="porcentaje Utilidad", config_parameter='cc_cotizaciones.utilidad')
    incentivos = fields.Float(default=0.01, string="porcentaje Incentivos", config_parameter='cc_cotizaciones.incentivos')


