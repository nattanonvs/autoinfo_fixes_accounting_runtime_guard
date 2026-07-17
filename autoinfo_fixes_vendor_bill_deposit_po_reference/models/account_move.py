from collections import defaultdict

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    po_origin = fields.Char("Source Document2", index=True, readonly=True, translate=True)
    origin_second = fields.Char(
        "Source Document (SO/PO)",
        index=True,
        readonly=True,
        translate=True,
    )
    deposit_po_ref = fields.Many2one(
        "purchase.order",
        string="PO Reference",
    )

    def _match_existing_lines_by_product(self, source_lines, target_lines):
        buckets = defaultdict(list)
        for source_line in source_lines.filtered(lambda line: line.product_id):
            buckets[source_line.product_id.id].append(source_line)

        matches = {}
        for target_line in target_lines.filtered(
            lambda line: not line.display_type and line.product_id
        ):
            bucket = buckets.get(target_line.product_id.id, [])
            matches[target_line] = bucket.pop(0) if bucket else False
        return matches

    @api.onchange("deposit_po_ref")
    def _onchange_deposit_po_ref_sync_links(self):
        for move in self:
            if (
                move.move_type != "in_invoice"
                or move.order_type != "deposit_payment"
                or not move.deposit_po_ref
            ):
                continue

            purchase_order = move.deposit_po_ref
            if "po_origin" in move._fields:
                move.po_origin = purchase_order.name

            matches = move._match_existing_lines_by_product(
                purchase_order.order_line,
                move.invoice_line_ids,
            )
            for target_line, source_line in matches.items():
                if not source_line:
                    continue
                if "purchase_line_id" in target_line._fields:
                    target_line.purchase_line_id = source_line
                if "vendor_source_doc" in target_line._fields:
                    target_line.vendor_source_doc = purchase_order.name

    @api.onchange("deposit_so_ref")
    def _onchange_deposit_so_ref_sync_links(self):
        for move in self:
            if (
                move.move_type != "out_invoice"
                or move.order_type != "deposit_payment"
                or not move.deposit_so_ref
            ):
                continue

            sale_order = move.deposit_so_ref
            if "origin_second" in move._fields:
                move.origin_second = sale_order.name

            matches = move._match_existing_lines_by_product(
                sale_order.order_line,
                move.invoice_line_ids,
            )
            for target_line, source_line in matches.items():
                if not source_line or "sale_line_ids" not in target_line._fields:
                    continue
                target_line.sale_line_ids = source_line


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    vendor_source_doc = fields.Char(string="Source")
