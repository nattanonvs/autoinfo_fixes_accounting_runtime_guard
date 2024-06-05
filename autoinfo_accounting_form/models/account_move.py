from odoo import fields, models, api


class account_move(models.Model):
    _inherit = 'account.move'

    deposit_so_ref = fields.Many2one('sale.order', string='SO Reference')