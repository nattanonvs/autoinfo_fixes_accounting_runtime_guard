from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    your_ref = fields.Char(string='Your Ref.')
    delivery_to_report = fields.Text(string='Delivery To')
    delivery_date_report = fields.Text(string='Delivery Date')
    warranty_report = fields.Text(string='Warranty')
