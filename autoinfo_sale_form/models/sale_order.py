from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    your_ref = fields.Char(string='Your Ref.')
    delivery_report = fields.Text(string='Delivery', required=True)
    payment_report = fields.Text(string='Payment', required=True)
    payment_report2 = fields.Text(string='Payment', required=True)
    payment_product = fields.Text(string='Product', required=True)
    payment_engineering = fields.Text(string='Engineering', required=True)
    validaity_report = fields.Integer(string='Validity(days)', required=True)
    warranty_report = fields.Integer(string='Warranty(months)', required=True)
    credit_report = fields.Integer(string='Credit(days)', required=True)
