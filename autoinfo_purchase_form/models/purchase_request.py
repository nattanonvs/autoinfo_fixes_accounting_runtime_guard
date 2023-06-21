from odoo import fields, models, api


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    dtr_purchase_delivery_to_report_id = fields.Many2one('dtr.purchase.delivery.to.report', string='Delivery To', required=False)
    delivery_to_report = fields.Text(string='Delivery To (Other)')
    delivery_date_report = fields.Date(string='Delivery Date')
    dtr_purchase_warranty_report_id = fields.Many2one('dtr.purchase.warranty.report', string='Warranty', required=False)
    dtr_purchase_term_report_id = fields.Many2one('dtr.purchase.term.report', string='Terms', required=False)
    dtr_purchase_shipment_report_id = fields.Many2one('dtr.purchase.shipment.report', string='Shipment', required=False)
    dtr_purchase_weight_report_id = fields.Many2one('dtr.purchase.weight.report', string='Weight', required=False)
    shipping_standard = fields.Float(string='Shipping Standard', default=0, digits='Product Price')
    tariff = fields.Float(string='Tariff', default=0, digits='Product Price')
