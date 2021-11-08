from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
from datetime import datetime, timedelta


def check_client_fields(cliente):
    if not cliente.tipo_cliente:
        return [False, "El cliente :{} no tiene valor en el campo tipo de cliente!".format(cliente.name)]

    elif cliente.tipo_cliente == "normal":

        if cliente.tarifa_base1 == 0.00 or cliente.porcentaje_ahorro == 0.00:
            return [False,
                    "El cliente :{} no tiene valor de tarifa Base 1 o Porcentaje de Ahorro!".format(cliente.name)]

    elif cliente.tipo_cliente == "especial" or cliente.tipo_cliente == "otro":
        if cliente.tarifa_base2 == 0.00 or cliente.tarifa_base3 == 0.00 or cliente.porcentaje_ahorro == 0.00:
            return [False,
                    "El cliente :{} no tiene valor de tarifa Base 2, tarifa Base 3 o Porcentaje de Ahorro!".format(
                        cliente.name)]

    elif cliente.tipo_cliente == "equinsa":
        if cliente.tarifa_base1 == 0.00:
            return [False, "El cliente :{} no tiene valor de tarifa Base 1!".format(cliente.name)]

    return [True]


class TableEntry(models.Model):
    _name = 'table.entry'

    name = fields.Char(string='Tabla de Datos ENEE', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), track_visibility='onchange')
    cliente = fields.Many2one('res.partner', string="Cliente")
    factura = fields.Many2one('account.move', string="Factura")

    # Datos ingresados
    f_mes_pertence = fields.Date(string="Fecha del Mes al que Pertenece", required=True)  # 4
    f_lectura_actual = fields.Date(string="Fecha Lectura Actual", required=True)  # 4
    f_lectura_anterior = fields.Date(string="Fecha Lectura Anterior", required=True)  # 5
    lectura_actual = fields.Float(string="Lectura Actual", required=True)  # 6
    lectura_anterior = fields.Float(string="Lectura Anterior", required=True)  # 7
    kwh_excendentes = fields.Float(string="KWH Excedentes y Consumidos", required=True)  # 9
    saldo_anterior_amortizacion = fields.Float(string="Saldo Anterior de Amortización", required=True)  # 19
    total_lps_enee = fields.Float(string="Total Factura Enee Lps", required=True)  # 20
    total_kwh_enee = fields.Float(string="Total Factura Enee Kwh", required=True)  # 21
    tasa_cambio = fields.Float(string="Tasa de Cambio", required=True)  # 22
    ahorro_acumulado_anterior = fields.Float(string="Ahorro Acumulado Anterior")  # 22

    # Datos Calculados
    tarifa_enee = fields.Float(string="Tarifa Enee", compute='get_tarifa_enee', stored=True)  # 1 check
    ahorro_tarifa = fields.Float(string="Ahorro en Tarifa", compute='get_ahorro_tarifa', stored=True)  # 3 check
    kwh_generados = fields.Float(string="KWH Generados", compute='get_kwh_generados', stored=True)  # 8 check
    kwh_facturados = fields.Float(string="KWH Facturados", compute='get_kwh_facturados', stored=True)  # 10 check
    subtotal = fields.Float(string="Total", compute='get_subtotal',
                            stored=True)  # 11 check mismo para el subtotal o precio del producto
    indicador_ambiental = fields.Float(string="Indicador Ambiental", compute='get_indicador_ambiental',
                                       store=True)  # 15 checks
    kilometros = fields.Float(string="Kilometros Manejados", compute='get_kilometros', store=True)  # 16 check
    co2_arbol = fields.Float(string="CO2 por arbol", compute='get_co2_arbol', store=True)  # 17 check
    galones_agua = fields.Float(string="Agua para Generar Energia Electrica", compute='get_galones_agua',
                                store=True)  # 18 check
    amortizacion_dolares = fields.Float(string="Amortización en Dolares", compute='get_amortizacion_dolares',
                                        store=True)  # 23 check
    saldo_actual_amortizacion = fields.Float(string="Saldo Actual de Amortización",
                                             compute='get_saldo_actual_amortizacion', store=True)  # 24 check
    total_amortizacion = fields.Float(string="total amortizacion", compute='get_total_amortizacion',
                                      stored=True)  # 12 total para el producto amortizacion
    total_oym_granja = fields.Float(string="operaciones y mantenimiento", compute='get_total_oym_granja',
                                    stored=True)  # 13  total para producto operaciony mantenimiento granja solar
    tarifa_equinsa = fields.Float(string="Tarifa Equinsa", compute='get_tarifa_equinsa', stored=True)
    ahorro_acumulado = fields.Float(string="Ahorro Acumulado", compute='get_ahorro_acumulado', stored=True)

    @api.model
    def create(self, vals):
        cliente = self.env['res.partner'].search([("id", '=', vals.get('cliente'))])
        check = check_client_fields(cliente)
        if not check[0]:
            raise Warning(_(check[1]))

        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('table.entry.sequence') or _('New')
        result = super(TableEntry, self).create(vals)

        return result

    # Item 1
    @api.depends('total_lps_enee', 'total_kwh_enee')
    def get_tarifa_enee(self):
        for record in self:
            if not (record.total_lps_enee > 0.00 and record.total_kwh_enee > 0.00):
                record.tarifa_enee = 0.00
            else:
                record.tarifa_enee = record.total_lps_enee / record.total_kwh_enee

    # Item 3
    @api.depends('tarifa_equinsa', 'tarifa_enee')
    def get_ahorro_tarifa(self):

        if not (self.tarifa_equinsa > 0.00 and self.tarifa_enee > 0.00):
            self.ahorro_tarifa = 0
        else:
            self.ahorro_tarifa = 1 - (self.tarifa_equinsa / self.tarifa_enee)

    # Item 8 bien
    @api.depends('lectura_actual', 'lectura_anterior')
    def get_kwh_generados(self):
        for rec in self:
            if not (rec.lectura_actual and rec.lectura_anterior):
                rec.kwh_generados = 0
            else:
                rec.kwh_generados = rec.lectura_actual - rec.lectura_anterior

    # Item 10 bien
    @api.depends('kwh_generados', 'kwh_excendentes')
    def get_kwh_facturados(self):
        for rec in self:
            if not (rec.kwh_generados > 0.00 and rec.kwh_excendentes > 0.00):
                rec.kwh_facturados = 0
            else:
                rec.kwh_facturados = rec.kwh_generados - rec.kwh_excendentes

    # Item 11
    @api.depends('tarifa_equinsa', 'kwh_facturados')
    def get_subtotal(self):
        if not (self.tarifa_equinsa > 0.00 and self.kwh_facturados > 0.00):
            self.subtotal = 0
        else:
            self.subtotal = self.tarifa_equinsa * self.kwh_facturados

    # Item 12
    @api.depends('subtotal')
    def get_total_amortizacion(self):
        if not (self.subtotal > 0.00):
            self.total_amortizacion = 0
        else:
            self.total_amortizacion = self.subtotal * 0.85

    # Item 13
    @api.depends('subtotal')
    def get_total_oym_granja(self):
        if not (self.subtotal > 0.00):
            self.total_oym_granja = 0
        else:
            self.total_oym_granja = (self.subtotal * 0.15) / 1.15

    # Item 15
    @api.depends('lectura_actual')
    def get_indicador_ambiental(self):
        if not (self.lectura_actual > 0.00):
            self.indicador_ambiental = 0
        else:
            self.indicador_ambiental = self.lectura_actual * 0.00073

    # Item 16
    @api.depends('lectura_actual')
    def get_kilometros(self):

        if not self.lectura_actual > 0.00:
            self.kilometros = 0
        else:
            self.kilometros = self.lectura_actual * 2.21

    # Item 17
    @api.depends('lectura_actual')
    def get_co2_arbol(self):

        if not self.lectura_actual > 0.00:
            self.co2_arbol = 0
        else:
            self.co2_arbol = self.lectura_actual * 0.0006919

    # Item 18
    @api.depends('lectura_actual')
    def get_galones_agua(self):

        if not self.lectura_actual > 0.00:
            self.galones_agua = 0
        else:
            self.galones_agua = self.lectura_actual * 0.3992

    # Item 23
    @api.depends('tasa_cambio', 'total_amortizacion')
    def get_amortizacion_dolares(self):

        if not (self.tasa_cambio > 0.00 and self.total_amortizacion > 0.00):
            self.amortizacion_dolares = 0
        else:
            self.amortizacion_dolares = self.total_amortizacion / self.tasa_cambio

    # Item 24
    @api.depends('amortizacion_dolares', 'saldo_anterior_amortizacion')
    def get_saldo_actual_amortizacion(self):

        if not (self.amortizacion_dolares > 0.00 and self.saldo_anterior_amortizacion > 0.00):
            self.saldo_actual_amortizacion = 0
        else:
            self.saldo_actual_amortizacion = self.saldo_anterior_amortizacion - self.amortizacion_dolares

    # Tarifa Equinsa
    @api.depends('cliente', 'tarifa_enee', 'tasa_cambio')
    def get_tarifa_equinsa(self):

        for record in self:
            if record.cliente:
                cliente = record.cliente
                porcentaje_ahorro = cliente.porcentaje_ahorro
                tarifa_enee = record.tarifa_enee
                tarifa_base1 = cliente.tarifa_base1 if cliente.tarifa_base1 else False
                tarifa_base2 = cliente.tarifa_base2 if cliente.tarifa_base2 else False
                tarifa_base3 = cliente.tarifa_base3 if cliente.tarifa_base3 else False
                c_enee = tarifa_enee * porcentaje_ahorro

                if cliente.tipo_cliente == "normal":
                    c_conversion = record.tasa_cambio * tarifa_base1
                    if c_enee < c_conversion:
                        record.tarifa_equinsa = c_enee
                    else:
                        record.tarifa_equinsa = c_conversion

                elif cliente.tipo_cliente == "especial":
                    if tarifa_enee > tarifa_base3:
                        record.tarifa_equinsa = c_enee

                    elif tarifa_enee < tarifa_base2:
                        record.tarifa_equinsa = tarifa_enee - 0.01

                    else:
                        record.tarifa_equinsa = tarifa_base2

                elif cliente.tipo_cliente == "otro":
                    if tarifa_enee > tarifa_base3:
                        record.tarifa_equinsa = c_enee
                    else:
                        record.tarifa_equinsa = tarifa_base2

                elif cliente.tipo_cliente == "equinsa":
                    record.tarifa_equinsa = tarifa_base1 * record.tasa_cambio

            else:
                record.tarifa_equinsa = 0.00

    @api.depends('cliente', 'tarifa_enee', 'tarifa_equinsa', 'kwh_facturados')
    def get_ahorro_acumulado(self):
        for record in self:
            ahorro_actual = 0  # Ahorro acumulado del registro actual
            ahorro_anterior = 0  # Ahorro acumulado de la data cargada anteriormente de este cliente
            valor_aa_anterior = 0  # ahorro acumulado ingresado manualmente que proviene del sistema anterior

            # este cliente ya se le ha ingresado el ahorro acumulado ?
            dom = [('cliente', '=', record.cliente.id), ('ahorro_acumulado_anterior', '>', 0)]
            data_aa_anterior = self.env['table.entry'].search(dom, order="create_date asc", limit=1)

            # si hasta ahorita lo ingresan
            if data_aa_anterior:
                valor_aa_anterior = data_aa_anterior.ahorro_acumulado_anterior

            # Si ya se habia ingresado
            elif record.ahorro_acumulado_anterior:
                valor_aa_anterior = record.ahorro_acumulado_anterior

            # Sacamos el ahorro anterior de la data en odoo del cliente
            if record.cliente:
                cliente = record.cliente
                dom = [('cliente', '=', cliente.id),('factura', '!=', False)]
                entries = self.env['table.entry'].search(dom)

                # Si este cliente ya tiene registros con facturas
                if entries:
                    for entry in entries:
                        ahorro_anterior += (entry.tarifa_enee - entry.tarifa_equinsa) * entry.kwh_facturados

            # Sacamos el ahorro acumulado del registro actual
            if record.tarifa_enee > 0.00 and record.tarifa_equinsa > 0.00 and record.kwh_facturados > 0.00:
                ahorro_actual = (record.tarifa_enee - record.tarifa_equinsa) * record.kwh_facturados

            # Sumatoria de todos los valores implicados en el ahorro acumulado
            record.ahorro_acumulado = ahorro_actual + ahorro_anterior + valor_aa_anterior
