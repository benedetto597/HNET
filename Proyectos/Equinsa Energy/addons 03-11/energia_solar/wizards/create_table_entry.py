from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreateTableEntry(models.TransientModel):
    _name = 'create.table.entry'

    # Datos ingesados
    cliente = fields.Many2one('res.partner', string="Cliente")
    factura = fields.Many2one('account.move', string="Factura")
    f_lectura_actual = fields.Date(string="Fecha Lectura Actual", required=True)  # 4
    f_lectura_anterior = fields.Date(string="Fecha Lectura Anterior", required=True)  # 5
    lectura_actual = fields.Float(string="Lectura Actual", required=True)  # 6
    lectura_anterior = fields.Float(string="Lectura Anterior", required=True)  # 7
    kwh_excendentes = fields.Float(string="KWH Excedentes y Consumidos", required=True)  # 9
    saldo_anterior_amortizacion = fields.Float(string="Saldo Anterior de Amortización", required=True)  # 19
    total_lps_enee = fields.Float(string="Total Factura Enee Lps", required=True)  # 20
    total_kwh_enee = fields.Float(string="Total Factura Enee Kwh", required=True)  # 21
    tasa_cambio = fields.Float(string="Tasa de Cambio", required=True)  # 22

    def _check_input_data(self, data):
        result = 0.00 in data.values()
        return result

    def create_table_entry(self):

        data = {
            'lectura_actual': self.lectura_actual,
            'lectura_anterior': self.lectura_anterior,
            'kwh_excendentes': self.kwh_excendentes,
            'saldo_anterior_amortizacion': self.saldo_anterior_amortizacion,
            'total_lps_enee': self.total_lps_enee,
            'total_kwh_enee': self.total_kwh_enee,
            'tasa_cambio': self.tasa_cambio,
        }
        result = self._check_input_data(data)

        if result:
            raise UserError(_('Favor llenar todos los campos!'))

        data.update({
            'cliente': self.cliente.id,
            'factura': self.factura.id,
            'f_lectura_actual': self.f_lectura_actual,
            'f_lectura_anterior': self.f_lectura_anterior,
        })

        raise UserError(_('Favor llenar todos los campos!'))

        tabla_entry = self.env['table.entry'].sudo().create(data)

        if tabla_entry:
            tabla_entry.onchange_tarifa_enee()
            tabla_entry.onchange_ahorro_tarifa()
            tabla_entry.onchange_kwh_generados()
            tabla_entry.onchange_kwh_facturados()
            tabla_entry.onchange_subtotal()
            tabla_entry.onchange_total_amortizacion()
            tabla_entry.onchange_total_oym_granja()
            tabla_entry.onchange_indicador_ambiental()
            tabla_entry.onchange_kilometros()
            tabla_entry.onchange_co2_arbol()
            tabla_entry.onchange_galones_agua()
            tabla_entry.onchange_amortizacion_dolares()
            tabla_entry.onchange_saldo_actual_amortizacion()

            self.factura.write({
                'data_entry': tabla_entry.id,
                'f_lectura_actual': self.f_lectura_actual,
                'f_lectura_anterior': self.f_lectura_anterior,
                'lectura_actual': self.lectura_actual,
                'lectura_anterior': self.lectura_anterior,
                'kwh_excendentes': self.kwh_excendentes,
                'saldo_anterior_amortizacion': self.saldo_anterior_amortizacion,
                'total_lps_enee': self.total_lps_enee,
                'total_kwh_enee': self.total_kwh_enee,
                'tasa_cambio': self.tasa_cambio,
            })

            self.factura.onchange_data_entry()
