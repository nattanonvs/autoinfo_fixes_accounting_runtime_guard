from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    deposit_po_ref = fields.Many2one(
        "purchase.order",
        string="PO Reference",
    )
