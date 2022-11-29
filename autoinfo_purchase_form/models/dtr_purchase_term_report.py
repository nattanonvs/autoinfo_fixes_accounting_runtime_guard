from odoo import fields, models, api


class DtrPurchaseTermReport(models.Model):
    _name = 'dtr.purchase.term.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Term Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
