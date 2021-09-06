from odoo import api, models

class ReportSaleDetails(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, config_ids=False, session_ids=False):
        res = super(ReportSaleDetails, self).get_sale_details()
        current_company = self.env.company
        custom_paperformat = self.env['report.paperformat'].search([('name', '=', 'Formato Factura Furiwa')], limit=1)
        
        if custom_paperformat:

            if current_company:
                if current_company.paperformat_id != custom_paperformat.id:
                    current_company.paperformat_id = custom_paperformat.id
            else: 
                return False
        else:
            return False
        return res
        



