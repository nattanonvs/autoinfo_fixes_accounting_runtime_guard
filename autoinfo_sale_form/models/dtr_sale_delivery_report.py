from odoo import fields, models, api


class DtrSaleDeliveryReport(models.Model):
    _name = 'dtr.sale.delivery.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Delivery Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
