from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    your_ref = fields.Char(string='Your Ref.')
    delivery_report = fields.Text(string='Delivery')
    payment_report = fields.Text(string='Payment')
    validaity_report = fields.Integer(string='Validity(days)')
    warranty_report = fields.Integer(string='Warranty(months)')
    credit_report = fields.Integer(string='Credit(days)')
