from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    your_ref = fields.Char(string='Your Ref.')
    dtr_sale_price_report_id = fields.Many2one('dtr.sale.price.report', string='Price', required=False)
    dtr_sale_delivery_report_id = fields.Many2one('dtr.sale.delivery.report', string='Delivery', required=False)
    dtr_sale_payment_product_report_id = fields.Many2one('dtr.sale.payment.product.report', string='Payment Product', required=False)
    dtr_sale_payment_engineering_report_id = fields.Many2one('dtr.sale.payment.engineering.report', string='Payment Engineering', required=False)
    dtr_sale_validity_report_id = fields.Many2one('dtr.sale.validity.report', string='Validity', required=False)
    dtr_sale_warranty_report_id = fields.Many2one('dtr.sale.warranty.report', string='Warranty', required=False)
    dtr_sale_credit_report_id = fields.Many2one('dtr.sale.credit.report', string='Credit', required=False)
