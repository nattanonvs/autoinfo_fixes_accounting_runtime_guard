from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    job_no = fields.Char(string='Job No.')
    job_type = fields.Selection([
        ('job', 'Job'),
        ('pm', 'PM'),
        ('service', 'Service')], string='Job Type', required=True, default='job')
    project_department_id = fields.Many2one('hr.department', 'Department', help="Select Requested Department", required=True,
        default=lambda self: self._default_department_id())
    project_sale_order_ids = fields.One2many('sale.order', 'customer_project', string='Sale Orders', copy=False)
    project_po_ids = fields.One2many('purchase.order', 'project_id', string='Purchase Orders', copy=False)

    def _default_department_id(self):
        if self.env.user.employee_ids:
            return self.env.user.employee_ids[0].department_id
        return self.env.ref('hr.dep_administration').id

    @api.model
    def create(self, vals):
        if (vals.get('job_no', '') == '' or not vals.get('job_no', '')) and vals.get('job_type') and vals.get('project_department_id'):
            department_id = self.env['hr.department'].sudo().browse(vals.get('project_department_id'))
            if vals.get('job_type') == 'job' and department_id.project_no_job_sequence_id:
                vals['job_no'] = department_id.project_no_job_sequence_id.next_by_id(sequence_date=vals.get('date_start'))
            elif vals.get('job_type') == 'pm' and department_id.project_no_pm_sequence_id:
                vals['job_no'] = department_id.project_no_pm_sequence_id.next_by_id(sequence_date=vals.get('date_start'))
            elif vals.get('job_type') == 'service' and department_id.project_no_service_sequence_id:
                vals['job_no'] = department_id.project_no_service_sequence_id.next_by_id(sequence_date=vals.get('date_start'))
        return super(ProjectProject, self).create(vals)
