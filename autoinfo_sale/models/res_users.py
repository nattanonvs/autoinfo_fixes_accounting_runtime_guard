from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    quotation_sequence_id = fields.Many2one('ir.sequence', string='Quotation Sequence', check_company=True)
