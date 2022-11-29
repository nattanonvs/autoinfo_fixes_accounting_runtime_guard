from odoo import fields, models, api


class DtrPurchaseWarrantyReport(models.Model):
    _name = 'dtr.purchase.warranty.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Warranty Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
