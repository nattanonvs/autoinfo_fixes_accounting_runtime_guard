# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


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

    @api.model
    def _prepare_purchase_order_line(self, po, item):
        if not item.product_id and not item.line_id.display_type: #--Edit--
            raise UserError(_("Please select a product for all lines"))
        product = item.product_id

        # Keep the standard product UOM for purchase order so we should
        # convert the product quantity to this UOM
        qty = item.product_uom_id._compute_quantity(
            item.product_qty, product.uom_po_id or product.uom_id
        )
        # Suggest the supplier min qty as it's done in Odoo core
        min_qty = item.line_id._get_supplier_min_qty(product, po.partner_id)
        qty = max(qty, min_qty)
        date_required = item.line_id.date_required
        vals = {
            "name": product.name,
            "order_id": po.id,
            "product_id": product.id,
            "product_uom": product.uom_po_id.id or product.uom_id.id,
            # "price_unit": 0.0,
            "product_qty": qty,
            "account_analytic_id": item.line_id.analytic_account_id.id,
            "purchase_request_lines": [(4, item.line_id.id)],
            "date_planned": datetime(
                date_required.year, date_required.month, date_required.day
            ),
            "move_dest_ids": [(4, x.id) for x in item.line_id.move_dest_ids],
            "display_type": item.line_id.display_type, #--Edit--
            "sequence": item.line_id.sequence, #--Edit--
            "autoinfo_list_price": item.line_id.autoinfo_list_price, #--Edit--
            "price_unit": item.line_id.price_unit, #--Edit--
            "discount": item.line_id.discount, #--Edit--
            "discount_type": item.line_id.discount_type, #--Edit--
            "taxes_id": [(6, 0, item.line_id.taxes_id.ids)], #--Edit--
            "price_subtotal": item.line_id.price_subtotal, #--Edit--
            "price_total": item.line_id.price_total, #--Edit--
            "price_tax": item.line_id.price_tax, #--Edit--
        }
        if item.line_id.analytic_tag_ids:
            vals["analytic_tag_ids"] = [
                (4, ati) for ati in item.line_id.analytic_tag_ids.ids
            ]
        self._execute_purchase_line_onchange(vals)
        return vals
