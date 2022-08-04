from odoo import fields, models, api


class autoinfo_employees_hr_department(models.Model):

    _inherit = 'hr.department'

    dtr_department_short = fields.Char(string='Department Short', copy=False)
