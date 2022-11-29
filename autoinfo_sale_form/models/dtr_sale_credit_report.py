from odoo import fields, models, api


class DtrSaleCreditReport(models.Model):
    _name = 'dtr.sale.credit.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Credit Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
