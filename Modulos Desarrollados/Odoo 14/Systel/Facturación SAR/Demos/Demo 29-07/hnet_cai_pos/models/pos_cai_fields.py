# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------

    @author ebenedetto@hnetw.com - HNET
    @date 27/07/2021
    @decription Datos exigidos en la factura SAR
    @name_file pos_cai_fields.py
    @version 1.0

----------------------------------------------------------------------------------------------------
"""
from odoo import fields, models, api, tools, _

class PosConfig(models.Model):
    """
        Campos para los ajustes del POS
        Configuración de los datos solicitados por el SAR en las facturas
    """
    _inherit = "pos.config"

    cai = fields.Char(string="CAI")
    rango = fields.Char(string="Rango Autorizado")
    rtn = fields.Char(string="RTN")
    razon = fields.Char(string="Razón Social")
    nombre = fields.Char(string="Nombre Comercial")
    correo = fields.Char(string="Correo")
    telefono = fields.Char(string="Teléfono")
    direccion = fields.Char(string="Dirección")
    rango_maximo = fields.Integer(string="Rango Máximo del CAI")
    fecha_expiracion = fields.Date(string="Fecha limite de Emisión")

    # Secuencia POS_CAI
    pos_order_sequence_prefix = fields.Char('Prefijo de la secuencia de la orden del POS')
    # Prefijo Ej, 000-001-01-00
    pos_order_sequence_id = fields.Many2one('ir.sequence', 'Secuencia de la orden del POS')

    @api.model
    def _update_pos_order_sequence_id(self, values):
        """
        Actualizar la secuencia de la orden utilizando el prefijo de la secuencia
            y rango autorizado
        """
        prefix = values.get('pos_order_sequence_prefix')
        if not prefix:
            return values
        seq_id = values.get('pos_order_sequence_id')
        if not seq_id:
            seq_id = self.env['ir.sequence'].create({
                'name': 'Pos order sequence',
                'padding': 8,
                'code': 'pos.order.custom',
                'prefix': prefix,
                'active': True,
                })
            values.update({'pos_order_sequence_id':seq_id})
        else:
            seq_obj = self.env['ir.sequence'].browse(seq_id)
            seq_obj.write({
                'prefix': prefix
            })
        return values

    @api.model
    def create(self, values):
        """
        !!! create --> Crea un nuevo registro en la base de datos
        Sobrescribir el método 'create' actualizando el prefijo y secuencia
        """
        self._update_pos_order_sequence_id(values)
        return super(PosConfig, self).create(values)

    def write(self, vals):
        """
        !!! write --> Sobrescribe un registro en la base de datos
        Sobrescribir el método 'write' actualizando el prefijo y secuencia
        """
        values = {}
        for conf in self:
            values = vals.copy()
            if conf.pos_order_sequence_id:
                values.update({'pos_order_sequence_id': conf.pos_order_sequence_id.id})
            self._update_pos_order_sequence_id(values)
        return super(PosConfig, self).write(values)
