from odoo import fields, models, api, tools, _


class PosConfig(models.Model):
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

    pos_order_sequence_prefix = fields.Char('Prefijo de la secuencia de la orden del POS')
    pos_order_sequence_id = fields.Many2one('ir.sequence', 'Secuencia de la orden del POS')

    @api.model
    def _update_pos_order_sequence_id(self, values):
        prefix = values.get('pos_order_sequence_prefix')
        if not prefix:
            return values
        seq_id = values.get('pos_order_sequence_id')
        if not seq_id:
            seq_id = self.env['ir.sequence'].create({
                'name':'Pos order sequence',
                'padding':8,
                'code':'pos.order.custom',
                'prefix': prefix,
                'active' : True,
                })
            values.update({'pos_order_sequence_id':seq_id})
        else:
            seq_obj = self.env['ir.sequence'].browse(seq_id)
            seq_obj.write({
                'prefix': prefix
            })
        return values

    @api.model
    def create(self,values):
        self._update_pos_order_sequence_id(values)
        return super(PosConfig, self).create(values)

    def write(self, vals):
        values = {}
        for conf in self:
            values = vals.copy()
            if conf.pos_order_sequence_id:
                values.update({'pos_order_sequence_id': conf.pos_order_sequence_id.id})
            self._update_pos_order_sequence_id(values)
        return super(PosConfig, self).write(values)
