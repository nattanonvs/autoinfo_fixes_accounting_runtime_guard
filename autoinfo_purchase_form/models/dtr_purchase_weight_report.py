from odoo import fields, models, api


class DtrPurchaseWeightReport(models.Model):
    _name = 'dtr.purchase.weight.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Weight Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
