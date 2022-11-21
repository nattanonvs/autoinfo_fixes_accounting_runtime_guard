from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    your_ref = fields.Char(string='Your Ref.')
    delivery_to_report = fields.Text(string='Delivery To')
    delivery_date_report = fields.Text(string='Delivery Date')
    warranty_report = fields.Text(string='Warranty')
    discount_report = fields.Float(string='Discount', default=0, digits='Product Price')
    shipping_standard = fields.Float(string='Shipping Standard', default=0, digits='Product Price')
    tariff = fields.Float(string='Tariff', default=0, digits='Product Price')
    weight_report = fields.Char(string='Weight')
