# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import pytz # Para obtener fecha y hora por region

class KitchenControl(models.Model):
    _name = 'kitchen.control'
    _description = 'hnet_kitchen_control.hnet_kitchen_control'
    _order = "name asc"

    # Campos requeridos -- PENDIENTE DE REVISION --
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), track_visibility='onchange')
    num_factura = fields.Char(string="Número de Factura")
    notes = fields.Char(string="Notas")
    fecha_pedido = fields.Datetime(string="Hora de Recepción del pedido")
    hora_elaboracion = fields.Char(string="Hora de Elaboración")
    ref_pedido = fields.Char(string="Referencia del Pedido")
    kitchen_control_lines = fields.One2many('kitchen.control.lines', 'kitchen_control_id', string="Order Lines")
    estado = fields.Selection([
        ("cocina", "Cocina"),
        ("facturacion", "Facturación"),
        ("despachado", "Despachado"),
    ], default='cocina', index=True)
    origen = fields.Many2one('crm.team', string="Origen")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    delivery_name = fields.Char(string="Identificador") # Se usa en create_kitchen_order

    """ ----------------------------- Campos innecesario -----------------------------
    finish_job = fields.Boolean(string="finish job flag", default=False)
    user_id = fields.Many2one('res.users', string="Enviado Por")
    sale_order_id = fields.Many2one('sale.order', string="Pedido")
    ------------------------------------------------------------------------------ """

    @api.model
    def create(self, vals):
        """ Crear la nueva secuencia para las ordenes de cocina """
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('kitchen.control.sequence') or _('New')
        result = super(KitchenControl, self).create(vals)
        return result

    def write(self, vals):
        """ Sobrescribir los registros existentes """

        # Estado actual de la orden de cocina
        estado_actual = self.estado

        # Estados permitidos 
        estados_permitidos = {
            'cocina': 'facturacion',
            'facturacion': 'despacho',
            'despacho': 'finalizado',
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

            # Si la orden de cocina se encuentra en facturación 
            if vals.get("estado") == "facturacion":
                tz_name = pytz.country_timezones['HN']
                tz = pytz.timezone(tz_name[0])
                now = datetime.now(tz)

                # Hora a utilizar a partir de la zona horaria
                dt_string = now.strftime("%H:%M %p") # Hora en texto
                vals.update({
                    'hora_elaboracion': dt_string
                })

        return super(KitchenControl, self).write(vals)

    @api.model
    def create_kitchen_order(self, order, notes=None):
        """ Crear Orden de cocina """

        # Id de la orden a partir del nombre de la orden (miOrden)
        order_id = self.env['sale.order'].search([('name', '=', order), ('procesado_pos', '=', False)])

        if not order_id:
            return [False, "orden no encontrada, No se creo el pedido en cocina, vuelva a cargar el pedido de cocina"]

        if len(order_id) <= 1:
            try:
                # nombre de la orden para usar el metodo create
                new_ko = self.new({'sale_order_id': order_id.id})
                
                new_ko._onchange_sale_order_id()

                # Convertir a texto los valores de la orden de cocina
                new_ko_vals = new_ko._convert_to_write(new_ko._cache)

                # Crear la nueva secuencia para la nueva orden de cocina
                ko = self.create(new_ko_vals)

                for orderline in ko.kitchen_control_lines: 

                    # Buscar si la linea de la orden tiene una nota asociada
                    if str(orderline.product_id.id) in notes:

                        # Obtener y guardar las notas en la linea de orden de la orden de cocina
                        nota_a_guardar = notes.get(str(orderline.product_id.id))
                        orderline.sudo().write({'notes': nota_a_guardar})

                # Marcar com oprocesado el pedido del ecommerce
                order_id.procesado_pos = True

            # Capturar el error
            except Exception as e:
                print(e)
                return [False, "No se pudo crear el pedido en cocina"]
            
            # La orden de cocina se creo exitosamente
            return [True, "Pedido {} creado correctamente!".format(ko.delivery_name), ko.name]

        return [False, "Mas de un registro con la misma referencia del pedido"]

    """
    @api.model
    def test(self):
        value = "Esto es el valor que tiene que sacar"
        print(value)
    """

    @api.model
    def estado_a_despachado(self):
        """ Cambiar a finalizado todos los pedidos al final del día 
            Tiene una vista asociada por lo tanto debe llevar el mismo nombre del metodo
        """
        recs = self.sudo().search([])
        for rec in recs:
            rec.sudo().write({
                'estado': 'despachado',
            })

    @api.model
    def eliminar_registros(self):
        """ Eliminar los registros a final de mes 
            Tiene una vista asociada por lo tanto debe llevar el mismo nombre del metodo
        """
        recs = self.sudo().search([])
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'kitchen.control.sequence')])
        sequence.sudo().write({'number_next_actual': 1})
        for rec in recs:
            rec.sudo().unlink()

    @api.model
    def get_kitchen_orders(self):
        """ Obtener las ordenes de cocina en estado de facturacion """
        result = []

        # Obtener el id de las ordenes que esten en estado de facturacion
        order_id = self.search([('estado', '=', 'facturacion')], order="id asc")
        if order_id:
            for order in order_id:
                new_vals = {
                    'order_id': order.id,
                    'kitchen_order_name': order.name,
                    'partner_name': order.partner_id.name,
                    'order_name': order.sale_order_id.display_name,
                    'source': order.origen.name,
                    'ref_pedido': order.ref_pedido or "N/A",
                }

                result.append(new_vals)
        print(result)
        return result

    @api.model
    def get_kitchen_orders_lines(self, ref):
        """ Obtener las lineas de una orden para mostrarlas al darle a 
                Mostrar pedido (En facturación)
        """
        result = []

        # Obtener la orden a partir de la referencia enviada
        order_id = self.search([('name', '=', ref)])

        if order_id:

            # Obtener las lineas de la orden de venta
            lines = self.env['sale.order.line'].search([('order_id', '=', order_id.sale_order_id.id)])

            for line in lines:
                new_vals = {
                    'product_id': line.product_id.id,
                    'product': line.product_id.name,
                    'qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'discount': line.discount,
                    'line_id': line.id,
                    'client_id': order_id.partner_id.id,

                }
                result.append(new_vals)

            return [result, order_id.display_name, order_id.hora_elaboracion]

    @api.model
    def procesar_pos_Kitchen_order(self, ref, num_factura):
        """ Confirmar que la orden ha sido pagada """

        # Obtener la orden a partir de la referencia
        order_id = self.search([('name', '=', ref)])

        if order_id:
            order_id.estado = 'despachado'
            order_id.num_factura = num_factura # num_factura se obtiene de order.name
            return order_id.estado
        return False

    """
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).estado.selection]
    """

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        """ Cambio de orden seleccionada """
        for rec in self:

            lines = [[5, 0, 0]]
            for line in rec.sale_order_id.order_line:
                vals = {
                    'product_id': line.product_id,
                    'product_qty': int(line.product_uom_qty),
                }
                lines.append([0, 0, vals])

            sale_order = rec.sale_order_id
            rec.kitchen_control_lines = lines
            rec.fecha_pedido = sale_order.date_order
            rec.partner_id = sale_order.partner_id
            rec.origen = sale_order.team_id
            ref_pedido = sale_order.client_order_ref if sale_order.client_order_ref else sale_order.display_name
            rec.ref_pedido = ref_pedido
            team = sale_order.team_id.name
            final_name = (team, ref_pedido, sale_order.partner_id.name) if sale_order.con_rtn else (team, ref_pedido)
            rec.delivery_name = " - ".join(final_name)

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """ Cuando se cambia el usuario """
        for rec in self:

            if rec.user_id:
                rec.estado = "despachado"

class KitchenControlLines(models.Model):
    _name = 'kitchen.control.lines'
    _description = 'hnet_kitchen_control_lines.hnet_kitchen_control_lines'

    kitchen_control_id = fields.Many2one('kitchen.control', string="kitchen_control_ID")
    product_id = fields.Many2one('product.product', string="Plato")
    product_qty = fields.Integer(string="Cantidad")
    notes = fields.Char(string="Nota")
