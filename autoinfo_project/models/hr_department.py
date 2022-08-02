from odoo import fields, models, api


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    project_no_job_sequence_id = fields.Many2one('ir.sequence', string='Project Job No.(Job) Sequence', check_company=True)
    project_no_pm_sequence_id = fields.Many2one('ir.sequence', string='Project Job No.(PM) Sequence', check_company=True)
    project_no_service_sequence_id = fields.Many2one('ir.sequence', string='Project Job No.(Service) Sequence', check_company=True)
