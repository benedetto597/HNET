# -*- coding: utf-8 -*-
import math
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    from num2words import num2words
except ImportError:
    raise ValidationError(
        'Por favor installe la libreria `num2words`.\n Como instalar la ultima version en Linux:\n 1. Descargelo de aqui https://github. com/savoirfairelinux/num2words \n 2. Descomprimir el archivo descargado\n 3. Chabiar el directorio de`num2words` y corre este comando: "python setup.py install"\n')


class AccountInvoice(models.Model):
    _inherit = ["account.move"]

    cai_shot = fields.Char("Cai", readonly=True)
    cai_expires_shot = fields.Date("Fecha Limite", readonly=True)
    min_number_shot = fields.Char("Numero Minimo", readonly=True)
    max_number_shot = fields.Char("Numero Maximo", readonly=True)
    amount_words = fields.Char('Cantidad  en Letras:',
                               help="El monto total de la factura en palabras es generado automáticamente por el sistema ... actualmente se admiten algunos idiomas",
                               compute='_compute_num2words')
    condition = fields.Char("Condition")
    envio = fields.Char("envio")
    ticket = fields.Char("Ticket")
    exempt_PO = fields.Char("N   Correlativo de orden de compra exenta:")
    exoneratedCard = fields.Char("N   Correlativo de constancia de registro exonerado:")
    regSag = fields.Char("N   Identificativo de registro de la SAG:")
    x_desc = fields.Monetary("Descuento y Rebajas Otorgadas")
    x_exonerado = fields.Monetary("Importe Exonerado")
    x_exento = fields.Monetary("Importe Exento")
    x_gravado15 = fields.Monetary("Importe Gravado 15%")
    x_gravado18 = fields.Monetary("Importe Gravado 18%")
    x_isv18 = fields.Monetary("Importe 18%")

    @api.depends('partner_id', 'currency_id', 'amount_total')
    def _compute_num2words(self):
        self.ensure_one()
        lastnum, firstnum = math.modf(self.amount_total)
        lastnum = lastnum * 100
        before_float = ''
        try:
            before_float = (num2words(firstnum, lang=self.partner_id.lang) + ' ' + (
                    self.currency_id.currency_name or '')).upper()
        except NotImplementedError:
            before_float = (num2words(firstnum, lang='en') + ' ' + (self.currency_id.currency_name or '')).upper()
        except TypeError:
            pass

        final_number = before_float
        if lastnum:
            final_number += ' con %s/100' % (round(float(lastnum)))
        self.amount_words = final_number.upper()

    _sql_constraints = [
        (
            'number', 'unique(number,company_id)',
            'El numero de factura debe ser unico, consulte la configuracion de la secuencia en el diario seleccionado!!')
    ]
    """
    def _check_balanced(self):
        res = super(AccountInvoice, self)._check_balanced()
        
        if self.type == "out_refund" and self.journal_id.refund_sequence_id:
            _logger.info("Es nota de credito")
            secuencia = self.journal_id.refund_sequence_id
        else:
            _logger.info("Es Factura")
            secuencia = self.journal_id.sequence_id

        if secuencia.fiscal_regime:
            if self.invoice_date > secuencia.expiration_date:
                secuencia.number_next_actual = secuencia.number_next_actual - 1
                raise Warning(_('la fecha de expiracion para esta secuencia es %s ') % secuencia.expiration_date)
            self.cai_shot = ''

            for regimen in secuencia.fiscal_regime:
                if regimen.selected:
                    self.cai_shot = regimen.cai.name
                    self.cai_expires_shot = regimen.cai.expiration_date
                    self.min_number_shot = secuencia.dis_min_value
                    self.max_number_shot = secuencia.dis_max_value

        return res
        """

    def action_post(self):
        if self.type in ("out_refund", "out_invoice"):
            if self.id is not False:
                # obtenemos el cai activo

                if self.type == "out_refund" and self.journal_id.refund_sequence_id:

                    secuencia = self.journal_id.refund_sequence_id
                else:

                    secuencia = self.journal_id.sequence_id

                if secuencia.fiscal_regime:
                    self.cai_shot = ''

                    for regimen in secuencia.fiscal_regime:
                        if regimen.selected:
                            self.cai_shot = regimen.cai.name
                            self.cai_expires_shot = regimen.cai.expiration_date
                            self.min_number_shot = secuencia.dis_min_value
                            self.max_number_shot = secuencia.dis_max_value

                today = date.today()
                dom = [('expiration_date', '>', today), ('company.id', '=', self.company_id.id),
                       ('tipo_cai', '=', self.type)]
                cai = self.env['dei.cai'].sudo().search(dom)
                fiscal_regime = None
                today = date.today()

                for fiscal in cai.fiscal_regimes:
                    if fiscal.para_facturacion:
                        fiscal_regime = fiscal

                if fiscal_regime:
                    next = None
                    for date_range in fiscal_regime.sequence.date_range_ids:

                        if date_range.date_to > today:
                            next = date_range.number_next_actual

                    hasta = fiscal_regime.hasta
                    expiration_date = fiscal_regime.sequence.expiration_date

                    if next is None or next > hasta or expiration_date <= today:
                        raise UserError(
                            'Ha llegado al rango máximo de impresión Autorizado o la fecha máxima de impresión expiró, favor revisar la configuración')

                    else:
                        res = super(AccountInvoice, self).action_post()
                        return res
                elif fiscal_regime is None:

                    raise UserError(
                        'Fecha máxima de impresión expiró o no ha selecionado la secuencia para facturar dentro del CAI, favor revisar la configuración')
            else:
                res = super(AccountInvoice, self).action_post()
                return res
        else:
            res = super(AccountInvoice, self).action_post()
            return res

