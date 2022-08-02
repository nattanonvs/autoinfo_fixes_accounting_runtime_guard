from odoo import fields, models, api


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    quotation_sequence_id = fields.Many2one('ir.sequence', string='Quotation Sequence', check_company=True)
