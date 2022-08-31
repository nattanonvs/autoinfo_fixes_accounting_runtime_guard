from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    jobno_sequence_id = fields.Many2one('ir.sequence', string='Job No. Sequence', check_company=True)
