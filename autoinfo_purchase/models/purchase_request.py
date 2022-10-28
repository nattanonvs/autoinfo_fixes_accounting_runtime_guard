from odoo import fields, models, api, _


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    job_no = fields.Char(string='Job No.', related='project_id.job_no')
    project_analytic_account_id = fields.Many2one('account.analytic.account', string='Project Analytic Account', related='project_id.analytic_account_id')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New') and 'department_id' in vals:
            department_id = self.env['hr.department'].browse(int(vals['department_id']))
            if department_id and department_id.pr_sequence_id:
                vals['name'] = department_id.pr_sequence_id.next_by_id(sequence_date=vals.get('date_start')) or '/'
        return super(PurchaseRequest, self).create(vals)
