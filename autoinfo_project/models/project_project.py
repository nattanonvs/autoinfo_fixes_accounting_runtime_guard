from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    job_no = fields.Char(string='Job No.')
