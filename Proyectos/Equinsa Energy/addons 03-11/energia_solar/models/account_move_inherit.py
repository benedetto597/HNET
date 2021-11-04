from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import json
import base64
import logging
_logger = logging.getLogger(__name__)


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically
    # said, the previous day of the first of next month
    return next_month - timedelta(days=next_month.day)

class AccountMoveDataInherit(models.Model):
    _inherit = 'account.move'

    # Relacion con los datos ingresados
    data_entry = fields.Many2one('table.entry', string="Datos de Factura ENEE")

    # Datos ingresados
    f_lectura_actual = fields.Date(string="Fecha Lectura Actual")  # 4
    f_lectura_anterior = fields.Date(string="Fecha Lectura Anterior")  # 5
    lectura_actual = fields.Float(string="Lectura Actual")  # 6
    lectura_anterior = fields.Float(string="Lectura Anterior")  # 7
    kwh_excendentes = fields.Float(string="KWH Excedentes y Consumidos")  # 9
    saldo_anterior_amortizacion = fields.Float(string="Saldo Anterior de Amortización")  # 19
    total_lps_enee = fields.Float(string="Total Factura Enee Lps")  # 20
    total_kwh_enee = fields.Float(string="Total Factura Enee Kwh")  # 21
    tasa_cambio = fields.Float(string="Tasa de Cambio")  # 22
    historicos_en_kwh = fields.Binary("Imagen Históricos de Consumos en Kwh")
    promedio_generacion_anual = fields.Binary("Imagen Promedio del Total de Generación Anual")

    def load_enee_transient(self):

        # TODO: Hacer mas robusta esta validacion para encontrar la data que no ha sido asignada a una factura
        data_entry = self.env['table.entry'].search([('cliente', '=', self.partner_id.id), ('factura', '=', False)])

        if data_entry:
            self.ensure_one()
            data = {
                'lectura_actual': data_entry.lectura_actual,
                'lectura_anterior': data_entry.lectura_anterior,
                'kwh_excendentes': data_entry.kwh_excendentes,
                'saldo_anterior_amortizacion': data_entry.saldo_anterior_amortizacion,
                'total_lps_enee': data_entry.total_lps_enee,
                'total_kwh_enee': data_entry.total_kwh_enee,
                'tasa_cambio': data_entry.tasa_cambio,
                'f_lectura_actual': data_entry.f_lectura_actual,
                'f_lectura_anterior': data_entry.f_lectura_anterior,
                'data_entry': data_entry.id,
            }
            data_entry.factura = self.id
            self.write(data)
            self.onchange_data_entry()

        else:
            raise UserError(_('Datos del cliente no encontrados'))

        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'create_table_entry_wizard_form',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.table.entry',
            'context': {'default_factura': self.id, 'default_cliente': self.partner_id.id},
            'target': 'new',
        }"""

    @api.onchange('invoice_line_ids')
    def onchange_price_subtotal_lin(self):
        exento = 0
        gravado = 0

        if self.invoice_line_ids:
            for line in self.invoice_line_ids:
                if not line.product_id.taxes_id:
                    exento += line.price_subtotal
                elif line.product_id.taxes_id:
                    gravado += line.price_subtotal

            self.x_exento = exento
            self.x_gravado15 = gravado

    @api.onchange('data_entry')
    def onchange_data_entry(self):

        if self.invoice_line_ids and self.data_entry:

            for line in self.invoice_line_ids:
                if "AMZN" in line.product_id.default_code:

                    line.price_unit = self.data_entry.total_amortizacion
                    line._onchange_price_subtotal()
                    line._onchange_balance()

                elif "OPYM" in line.product_id.default_code:
                    line.price_unit = self.data_entry.total_oym_granja
                    line._onchange_price_subtotal()
                    line._onchange_balance()

        self.onchange_price_subtotal_lin()
        self.with_context(check_move_validity=False)._recompute_dynamic_lines(recompute_all_taxes=True,
                                                                              recompute_tax_base_amount=True)

    def get_charts_data(self):

        if self.data_entry:

            if not self.invoice_date:
                raise UserError("Favor asignar Fecha a la factura.")

            # buscar en el mismo year datetime.now().year
            last_day = last_day_of_month(self.invoice_date)
            initial = datetime(day=1, month=1, year=self.invoice_date.year).date()
            final = datetime(day=last_day.day, month=self.invoice_date.month, year=self.invoice_date.year).date()

            # domino condicional para realizar la busqueda
            dom = [("cliente", "=", self.partner_id.id),
                   ("f_mes_pertence", ">=", initial),
                   ("f_mes_pertence", "<=", final),
                   ("factura", "!=", False)]

            # Realizamos la busqueda y la ordenamos de enero a diciembre
            table_entry = self.env["table.entry"]
            table_entry_recs = table_entry.search(dom, order="f_mes_pertence asc")

            # Inicializamos el arreglo del bar graph
            ee_bar = [0 for val in range(12)]
            enee_bar = [0 for val in range(12)]

            # Recorremos los rec para sacar la info del chart
            total_enee_pie = 0
            total_ee_pie = 0
            highest = []
            if table_entry_recs:
                for rec in table_entry_recs:
                    # Sacamos la fecha a la cual pertence esta data
                    fecha_recibo = rec.f_mes_pertence

                    # hacemos la sumatoria de cada valor
                    total_enee_pie += round(rec.total_kwh_enee)
                    total_ee_pie += round(rec.kwh_facturados)

                    # guardamos los respectivos valores en cada lugar
                    ee_bar[fecha_recibo.month - 1] = round(rec.kwh_facturados)
                    enee_bar[fecha_recibo.month - 1] = round(rec.total_kwh_enee)
                    highest_temp = round(rec.kwh_facturados + rec.total_kwh_enee)
                    # Sacamos el de energia total del mes
                    highest.append(highest_temp)

                # sacamos el total global
                cien_del_pie = total_enee_pie + total_ee_pie

                # Sacamos porcentajes
                procentaje_ee = round(total_ee_pie/cien_del_pie * 100)
                procentaje_enee = round(total_enee_pie/cien_del_pie * 100)

                # Sacamos el valor maximo para la grafica de barra
                bar_graph_max = max(highest) + 10000
                return {
                    "ee_bar": ee_bar,
                    "enee_bar": enee_bar,
                    "procentaje_ee": procentaje_ee,
                    "procentaje_enee": procentaje_enee,
                    "bar_graph_max": bar_graph_max
                }

            else:
                return False
        else:
            raise UserError("No se encontraron registros para los gráficos")

    def btn_generar_graficos(self):

        #verificar si ya esta la data_entry
        if not self.data_entry:
            raise UserError("Para generar los gráficos es necesario haber cargado la información necesaria.")

        # aqui mandamos a generar la data

        charts_data = self.get_charts_data()

        if not charts_data:
            raise UserError("No se encontro información  relacionado a este cliente para generar las graficas")

        # bar chart
        ee_bar = charts_data["ee_bar"]
        enee_bar = charts_data["enee_bar"]
        bar_graph_max = charts_data["bar_graph_max"]

        bar_chart = {
            "chart": {
                "type": 'column',
                "borderColor": "#d0d4d6",
                "borderWidth": 1,

            },
            "credits": "false",
            "title": {
                "text": 'Historico de Consumo en KWH'
            },
            "xAxis": {
                "categories": ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            },
            "yAxis": {
                "min": 0,
                "max": bar_graph_max,
                "title": ""
            },
            "tooltip": {
                "pointFormat": '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
                "shared": "true"
            },
            "plotOptions": {
                "column": {
                    "stacking": 'amount',
                    "dataLabels": {
                        "enabled": "true",
                        "style": {
                            "fontSize": '12px',

                        }
                    },
                }
            },

            "series": [
                {
                    "name": 'Energia KWH EE',
                    "data": ee_bar,
                    "color": '#a8d18d',
                    "shadow": {
                        "color": 'black',
                        "width": 1,

                    }
                },
                {
                    "name": 'Energia KWH ENEE',
                    "data": enee_bar,
                    "color": '#ffff01',
                }
            ]
        }
        bar_data = {
            "options": json.dumps(bar_chart),
            "filename": "barchart",
            "type": 'image/png',
            "async": "true"
        }

        # Pie chart
        ee_pie = charts_data["procentaje_ee"]
        enee_pie =charts_data["procentaje_enee"]
        pie_chart = {
            "chart": {
                "type": 'pie',
                "borderColor": "#d0d4d6",
                "borderWidth": 1,
            },
            "credits": "false",
            "title": {
                "text": 'Promedio del Total de Generación Anual'
            },
            "tooltip": {
                "pointFormat": '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            "accessibility": {
                "point": {
                    "valueSuffix": '%'
                }
            },
            "plotOptions": {
                "pie": {
                    "dataLabels": {
                        "enabled": "true",
                        "format": '<b>{point.name}</b>: {point.percentage:.1f} %',
                        "style": {
                            "fontSize": '15px'
                        }
                    },
                    "showInLegend": "true",
                    "borderColor": '#000000'
                }
            },
            "series": [{
                "data": [{
                    "name": '(%)ENEE',
                    "color": '#ffff01',
                    "y": enee_pie,
                }, {
                    "name": '(%)EQUINSA ENERGY',
                    "color": '#a8d18d',
                    "y": ee_pie
                }]
            }]
        }
        pie_data = {
            "options": json.dumps(pie_chart),
            "filename": "piechart",
            "type": 'image/png',
            "async": "true"
        }

        # Realizamos las consultas al API
        url = "http://export.highcharts.com/"

        try:
            # call the API
            response_bar = requests.request("POST", url, data=bar_data, timeout=10)
            response_pie = requests.request("POST", url, data=pie_data, timeout=10)
        except Exception as e:
            _logger.info("ERROR AL GENERAR LOS GRAFICOS:{}".format(e))
            raise UserError("ERROR AL GENERAR LOS GRAFICOS DE FACTURA")

        if response_bar:
            if response_bar.status_code == 200:
                result = url + response_bar.text
                img = base64.b64encode(requests.get(result).content)
                self.historicos_en_kwh = img

        if response_pie:
            if response_pie.status_code == 200:
                result = url + response_pie.text
                img = base64.b64encode(requests.get(result).content)
                self.promedio_generacion_anual = img

