# -*- coding: utf-8 -*-

from odoo import models, api
from datetime import date, timedelta
from odoo.exceptions import Warning


class ValidateCai(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # obtenemos el cai activo
        dom = [('name', '=', self.cai_shot)]
        cai = self.env['dei.cai'].sudo().search(dom)
        fiscal_regime = None
        today = date.today()

        for fiscal in cai.fiscal_regimes:
            if fiscal.selected:
                fiscal_regime = fiscal

        if fiscal_regime:

            next = None
            for date_range in fiscal_regime.sequence.date_range_ids:

                if date_range.date_to > today:
                    next = date_range.number_next_actual

            hasta = fiscal_regime.hasta
            expiration_date = fiscal_regime.sequence.expiration_date

            if next > hasta or expiration_date < today or next is None:
                raise Warning(
                    'Ha llegado al rango máximo de impresión Autorizado o la fecha máxima de impresión expiró, favor revisar la configuración')

            else:
                res = super(ValidateCai, self).action_post()
                return res
