from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestStockPickingSalePersonTier(TransactionCase):
    def test_stock_picking_exposes_sale_person_user_id(self):
        self.assertIn(
            "sale_person_user_id",
            self.env["stock.picking"]._fields,
            "stock.picking should expose sale_person_user_id for the linked salesperson.",
        )

    def test_stock_picking_exposes_reviewer_ids(self):
        self.assertIn(
            "reviewer_ids",
            self.env["stock.picking"]._fields,
            "stock.picking should expose reviewer_ids so tier reviewers remain discoverable.",
        )
