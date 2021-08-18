# -*- coding: utf-8 -*-

"""
!!!! Identificar los métodos involucrados en los cambios a realizar 
!!!! Identificar los objetos involucrados en los cambios a realizar 

!!!! Realizar los cambios en el modelo PY

Modificar lo visual para que realice la tarea de dashboard
Obtener los datos y mostrarlos

Realizar los cambios en access
"""

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import pytz # Para obtener fecha y hora por region


class PosPedidosCocina(models.Model):
    _name = 'pos_pedidos_cocina'
    _description = 'pos_pedidos_cocina'

    referencia = fields.Char(string='Referencia', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), track_visibility='onchange')
    fecha_pedido = fields.Datetime(string="Hora de Recepción del pedido")
    hora_pedido = fields.Char(string="Hora del pedido")
    id_orden = fields.Char(string="Número de orden")
    prductos = fields.One2many('pos_pedidos_cocina.lines', 'pedidos_cocina_id', string="Order Lines")
    origen = fields.Many2one('crm.team', string="Origen")
    cliente = fields.Many2one('res.partner', string="Cliente")
    estado = fields.Selection([
        ("cocina", "Cocina"),
        ("facturacion", "Facturación"),
        ("despachado", "Despachado"),
    ], default='cocina', index=True)

    ### --------------------------------------- Crear, modificar y eliminar registros ---------------------------------------
    @api.model
    def create(self, vals):
        """ Crear el registro nuevo y la secuencia para los pedidos de cocina """
        if vals.get('referencia', _('New')) == _('New'):
            vals['referencia'] = self.env['ir.sequence'].next_by_code('pos_pedidos_cocina.sequence') or _('New')
        result = super(PosPedidosCocina, self).create(vals)
        return result

    def write(self, vals):
        """ Sobrescribir los registros existentes 
            Cambiar el estado de un pedido de cocina """

        # Estado actual de la orden de cocina
        estado_actual = self.estado

        # Estados permitidos 
        estados_permitidos = {
            'cocina': 'facturacion',
            'facturacion': 'despachado',
            'despachado': 'finalizado',
        }

        # Si el registro tiene estados
        if 'estado' in vals:
            llave_estado, siguiente_estado_permitido = None, None

            # Nuevo estado 
            nuevo_estado = vals.get("estado")

            # Obtener el estado permitido a partir del estado actual
            for llave, valor in estados_permitidos.items():
                if llave == estado_actual:
                    # Estado actual encontrado en los permitidos
                    llave_estado, siguiente_estado_permitido = llave, valor

            if estado_actual == llave_estado:
                if nuevo_estado != siguiente_estado_permitido:
                    if estado_actual == 'despachado':
                        raise Warning(_('No se permite cambiar el estado una vez que se ha Despachado'))
                    else:
                        raise Warning(_('De {} solo se permite pasar el estado a {}'.format(estado_actual, siguiente_estado_permitido)))

        return super(PosPedidosCocina, self).write(vals)
        
    @api.model
    def eliminar_registros(self):
        """ Eliminar los registros a final de mes 
            Tiene una vista asociada por lo tanto debe llevar el mismo nombre del metodo
        """
        recs = self.sudo().search([])
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'pos_pedidos_cocina.sequence')])
        sequence.sudo().write({'number_next_actual': 1})
        for rec in recs:
            rec.sudo().unlink()

    ### --------------------------------------- Cambiar el estado del pedido de cocina ---------------------------------------
    @api.model
    def estado_a_despachado(self):
        """ Cambiar a despachado todos los pedidos al final del día 
            Tiene una vista asociada por lo tanto debe llevar el mismo nombre del metodo """
            
        recs = self.sudo().search([])
        for rec in recs:
            rec.sudo().write({
                'estado': 'despachado',
            })

    @api.model
    def estado_a_facturacion(self, record):
        """ Cambiar a despachado todos los pedidos al final del día 
            Tiene una vista asociada por lo tanto debe llevar el mismo nombre del metodo """
            
        recs = self.sudo().search([])
        for rec in recs:
            if(record.referencia == rec.referencia):
                rec.sudo().write({
                    'estado': 'facturacion',
                })

    ### --------------------------------------- Crear pedido de cocina ---------------------------------------
    @api.model
    def create_pedido_cocina(self, id_orden, orderlines, origen, cliente):
        """ Crear pedido de cocina 
                Campos que vienen como parametros: 
                --> id_orden
                --> prductos u orderlines
                --> origen
                --> cliente
        """
        if(id_orden and origen):
            try:
                tz_name = pytz.country_timezones['HN']
                tz = pytz.timezone(tz_name[0])
                now = datetime.now(tz)

                # Hora a utilizar a partir de la zona horaria
                dt_string = now.strftime("%H:%M %p") # Hora en texto

                self.create({
                    "fecha_pedido": now,
                    "hora_pedido": dt_string, 
                    "id_orden": id_orden,
                    "prductos": orderlines,
                    "origen": origen, 
                    "cliente": cliente,
                })
                return True

            except Exception as e:
                return "Error: {}".format(e)

    ### --------------------------------------- Obtener los pedidos de cocina ---------------------------------------
    @api.model
    def get_pedidos_cocina(self, estado = None):
        """ Obtener los registros de los pedidos de cocina a partir de su estado 
            El "estado" puede ser: 
                --> cocina
                --> facturacion
                --> despachado

            Si no se tiene un esatado como parametro se devuelven todos los pedidos
        """

        result = []

        if not estado: 
            # Obtener todos los registros
            records = self.sudo().search([])
        else:
            dom = [("estado", "=", estado)]
            # Registros con el estado requerido
            records = self.sudo().search(dom)
        
        if records:
            try:
                for rec in records:
                    result.append(rec)
            except Exception as e:
                print('Error al obtener los registros --> {}'.format(e))
                _return = [False, "No se pudieron obtener los pedidos de cocina"]
                result.append(_return)

        print(result)
        return result

    @api.model
    def get_pedidos_cocina_lines(self, ref):
        """ Obtener las lineas de una orden para mostrarlas al darle Mostrar pedido """
        result = []
    
        dom = [("referencia", "=", ref)]
        # Registro a partir de la referencia
        record = self.sudo().search(dom)

        if record:
            try: 
                # Obtener las lineas de la orden de venta
                lines = record['productos']

                for line in lines:
                    new_vals = {
                        'producto_id': line.id,
                        'producto_nombre': line.product.display_name,
                        'cantidad': line.quantity,
                        'precio_unidad': line.price,
                        'descuento': line.discount,
                        'nota': line.note,
                    }
                    result.append(new_vals)

            except Exception as e:
                print('Error al obtener las lineas de los registros --> {}'.format(e))
                _return = [False, "No se pudieron obtener las líneas de los pedidos de cocina"]
                result.append(_return)

            return result
    
    ### --------------------------------------- Obtener los equipos de ventas ---------------------------------------
    @api.model
    def get_equipo_de_ventas(self):
        """ Obtener equipos de venta """
        equipo_de_ventas = self.env['crm.team'].sudo().search([])
        results = []
        if equipo_de_ventas:
            for rec in equipo_de_ventas:
                results.append(rec.name)
            return results

    def test_create(self):
        
        self.create({
                    "fecha_pedido": '06/06/2021',
                    "hora_pedido": "10:41:26", 
                    "id_orden": "00006-718-0197",
                    "prductos": [],
                    "origen": 'Hugo', 
                    "cliente": 'Hugo',
                })


class InheritClose(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_closing_control(self):
        """ Eliminar los pedidos de cocina al cerrar la sesión del punto de venta """
        res = super(InheritClose, self).action_pos_session_closing_control()
        pedidos_cocina = self.env['pos_pedidos_cocina'].search([])
        if pedidos_cocina:
            for pedido in pedidos_cocina:
                pedido.sudo().unlink()

        return res


class CrmTeamInherit(models.Model):
    _inherit = 'crm.team'

    cargar_pos = fields.Boolean("Equipo de venta Para delivery", default=False)


class PedidosCocinaLines(models.Model):
    _name = 'pos_pedidos_cocina.lines'
    _description = 'hnet_pos_pedidos_cocina.hnet_pos_pedidos_cocina_lines'

    pedidos_cocina_id = fields.Many2one('pos_pedidos_cocina', string="pos_pedidos_cocina_ID")
    producto_id = fields.Many2one('product.product', string="Producto")
    producto_qty = fields.Integer(string="Cantidad")
    notas = fields.Char(string="Nota")