from odoo import fields, models, api


class DtrSaleWarrantyReport(models.Model):
    _name = 'dtr.sale.warranty.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Warranty Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
