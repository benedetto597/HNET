from odoo import models
from ast import literal_eval


class ProjectProjectInherit(models.Model):
    _inherit = "project.project"

    def open_stock_moves(self):
        moves = self.env['stock.move'].search([('analytic_account_id', '=', self.analytic_account_id.id)])
        domain = [('id', 'in', moves.mapped("id"))]
        action = self.env.ref('resumen_pres_ent.stock_move_cost_action').read()[0]
        context = literal_eval(action['context'])
        context.update(self.env.context)
        res = dict(action, domain=domain, context=context)
        return res
