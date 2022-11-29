from odoo import fields, models, api


class DtrSaleValidityReport(models.Model):
    _name = 'dtr.sale.validity.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Validity Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
