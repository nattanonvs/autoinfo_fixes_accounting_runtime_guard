from odoo import fields, models, api


class DtrPurchaseDeliveryToReport(models.Model):
    _name = 'dtr.purchase.delivery.to.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Delivery To Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
