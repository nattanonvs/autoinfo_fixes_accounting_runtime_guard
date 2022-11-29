from odoo import fields, models, api


class DtrPurchaseShipmentReport(models.Model):
    _name = 'dtr.purchase.shipment.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Shipment Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
