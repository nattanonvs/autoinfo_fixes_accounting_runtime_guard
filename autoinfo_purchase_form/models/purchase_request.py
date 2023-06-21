from odoo import fields, models, api


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    attention_id = fields.Many2one('res.users', string='Attention', tracking=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, 
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")

    dtr_purchase_delivery_to_report_id = fields.Many2one('dtr.purchase.delivery.to.report', string='Delivery To', required=False)
    delivery_to_report = fields.Text(string='Delivery To (Other)')
    delivery_date_report = fields.Date(string='Delivery Date')
    dtr_purchase_warranty_report_id = fields.Many2one('dtr.purchase.warranty.report', string='Warranty', required=False)
    dtr_purchase_term_report_id = fields.Many2one('dtr.purchase.term.report', string='Terms', required=False)
    dtr_purchase_shipment_report_id = fields.Many2one('dtr.purchase.shipment.report', string='Shipment', required=False)
    dtr_purchase_weight_report_id = fields.Many2one('dtr.purchase.weight.report', string='Weight', required=False)
    shipping_standard = fields.Float(string='Shipping Standard', default=0, digits='Product Price')
    tariff = fields.Float(string='Tariff', default=0, digits='Product Price')


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    partner_id = fields.Many2one('res.partner', related='request_id.partner_id', string='Partner', readonly=True, store=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
