from odoo import fields, models, api


class DtrSalePriceReport(models.Model):
    _name = 'dtr.sale.price.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Price Report'

    name = fields.Text(string='Description', required=True)
