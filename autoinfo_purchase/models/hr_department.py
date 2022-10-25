from odoo import fields, models, api


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    pr_sequence_id = fields.Many2one('ir.sequence', string='PR Sequence', check_company=True)
    po_sequence_id = fields.Many2one('ir.sequence', string='PO Sequence', check_company=True)
