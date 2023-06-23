# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit ='purchase.request.line.make.purchase.order'

    def make_purchase_order(self):
        vals = super(PurchaseRequestLineMakePurchaseOrder, self).make_purchase_order()
        for item in self.item_ids:
            request_id = item.line_id.request_id

        for item in self.env['purchase.order'].browse(vals['domain'][0][2]):
            item.dtr_purchase_delivery_to_report_id = request_id.dtr_purchase_delivery_to_report_id
            item.delivery_to_report = request_id.delivery_to_report
            item.delivery_date_report = request_id.delivery_date_report
            item.dtr_purchase_warranty_report_id = request_id.dtr_purchase_warranty_report_id
            item.dtr_purchase_term_report_id = request_id.dtr_purchase_term_report_id
            item.dtr_purchase_shipment_report_id = request_id.dtr_purchase_shipment_report_id
            item.dtr_purchase_weight_report_id = request_id.dtr_purchase_weight_report_id
            item.shipping_standard = request_id.shipping_standard
            item.tariff = request_id.tariff
            item.attention_id = request_id.attention_id
            item.your_ref = request_id.your_ref
            item.project_id = request_id.project_id
        return vals
