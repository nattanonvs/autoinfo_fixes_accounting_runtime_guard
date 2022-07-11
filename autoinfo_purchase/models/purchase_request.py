from odoo import fields, models, api


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    job_no = fields.Char(string='Job No.', related='project_id.job_no')
