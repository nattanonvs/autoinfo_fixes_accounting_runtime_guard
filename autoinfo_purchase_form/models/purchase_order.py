from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    your_ref = fields.Char(string='Your Ref.')
    delivery_to_report = fields.Text(string='Delivery To (Other)')
    delivery_date_report = fields.Date(string='Delivery Date')
    discount_report = fields.Float(string='Discount', default=0, digits='Product Price')
    shipping_standard = fields.Float(string='Shipping Standard', default=0, digits='Product Price')
    tariff = fields.Float(string='Tariff', default=0, digits='Product Price')
    dtr_purchase_warranty_report_id = fields.Many2one('dtr.purchase.warranty.report', string='Warranty', required=True)
    dtr_purchase_delivery_to_report_id = fields.Many2one('dtr.purchase.delivery.to.report', string='Delivery To', required=True)
    dtr_purchase_term_report_id = fields.Many2one('dtr.purchase.term.report', string='Terms', required=True)
    dtr_purchase_shipment_report_id = fields.Many2one('dtr.purchase.shipment.report', string='Shipment', required=True)
    dtr_purchase_weight_report_id = fields.Many2one('dtr.purchase.weight.report', string='Weight', required=True)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    autoinfo_list_price = fields.Float(string='List Price', digits='Product Price', related='product_id.autoinfo_list_price')

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        res = super(PurchaseOrderLine, self)._onchange_quantity()
        if self.product_id:
            self.price_unit = self.product_id.autoinfo_list_price
        return res
