from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def cancel_expired_so(self):
        sos = self.search([]).filtered(lambda r: r.state in ['draft', 'sent'] and r.validity_date)
        if sos:
            _logger.info("CANT SOS: %s" % (len(sos)))
            for so in sos:
                if so.validity_date < fields.Date.today():
                    so.action_cancel()

                else:
                    _logger.info(" ".join(("orden:", so.name, "aun no expira")))
        else:
            _logger.info("No hay Cotizaciones expiradas")


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    def copy_data(self, default=None):
        product = self.product_id
        if product:
            self.product_id_change()

        return super(SaleOrderLineInherit, self).copy_data(default)
