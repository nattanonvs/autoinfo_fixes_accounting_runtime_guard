# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit ='purchase.request.line.make.purchase.order'

    def make_purchase_order(self):
        res = []
        purchase_obj = self.env["purchase.order"]
        po_line_obj = self.env["purchase.order.line"]
        pr_line_obj = self.env["purchase.request.line"]
        purchase = False

        for item in self.item_ids:
            line = item.line_id
            if item.product_qty <= 0.0 and not line.display_type: #--Edit--
                raise UserError(_("Enter a positive quantity."))
            if self.purchase_order_id:
                purchase = self.purchase_order_id
            if not purchase:
                po_data = self._prepare_purchase_order(
                    line.request_id.picking_type_id,
                    line.request_id.group_id,
                    line.company_id,
                    line.origin,
                )
                purchase = purchase_obj.create(po_data)

            # Look for any other PO line in the selected PO with same
            # product and UoM to sum quantities instead of creating a new
            # po line
            domain = self._get_order_line_search_domain(purchase, item)
            available_po_lines = po_line_obj.search(domain)
            new_pr_line = True
            # If Unit of Measure is not set, update from wizard.
            if not line.product_uom_id:
                line.product_uom_id = item.product_uom_id
            # Allocation UoM has to be the same as PR line UoM
            alloc_uom = line.product_uom_id
            wizard_uom = item.product_uom_id
            if available_po_lines and not item.keep_description:
                new_pr_line = False
                po_line = available_po_lines[0]
                po_line.purchase_request_lines = [(4, line.id)]
                po_line.move_dest_ids |= line.move_dest_ids
                po_line_product_uom_qty = po_line.product_uom._compute_quantity(
                    po_line.product_uom_qty, alloc_uom
                )
                wizard_product_uom_qty = wizard_uom._compute_quantity(
                    item.product_qty, alloc_uom
                )
                all_qty = min(po_line_product_uom_qty, wizard_product_uom_qty)
                self.create_allocation(po_line, line, all_qty, alloc_uom)
            else:
                po_line_data = self._prepare_purchase_order_line(purchase, item)
                if item.keep_description or line.display_type: #--Edit--
                    po_line_data["name"] = item.name
                po_line = po_line_obj.create(po_line_data)
                po_line_product_uom_qty = po_line.product_uom._compute_quantity(
                    po_line.product_uom_qty, alloc_uom
                )
                wizard_product_uom_qty = wizard_uom._compute_quantity(
                    item.product_qty, alloc_uom
                )
                all_qty = min(po_line_product_uom_qty, wizard_product_uom_qty)
                self.create_allocation(po_line, line, all_qty, alloc_uom)
            # TODO: Check propagate_uom compatibility:
            new_qty = pr_line_obj._calc_new_qty(
                line, po_line=po_line, new_pr_line=new_pr_line
            )
            po_line.product_qty = new_qty
            po_line._onchange_quantity()
            po_line.price_unit = po_line_data['price_unit']
            # The onchange quantity is altering the scheduled date of the PO
            # lines. We do not want that:
            date_required = item.line_id.date_required
            po_line.date_planned = datetime(
                date_required.year, date_required.month, date_required.day
            )
            res.append(purchase.id)

        # -----------------------------------
        for item in self.item_ids:
            request_id = item.line_id.request_id

        for item in self.env['purchase.order'].browse(res):
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
            item.trade_discount = request_id.trade_discount
            item.trade_discount_type = request_id.trade_discount_type
        # -----------------------------------

        return {
            "domain": [("id", "in", res)],
            "name": _("RFQ"),
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "view_id": False,
            "context": False,
            "type": "ir.actions.act_window",
        }

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
            "is_trade_discount": item.line_id.is_trade_discount, #--Edit--
        }
        if item.line_id.analytic_tag_ids:
            vals["analytic_tag_ids"] = [
                (4, ati) for ati in item.line_id.analytic_tag_ids.ids
            ]
        self._execute_purchase_line_onchange(vals)
        return vals
