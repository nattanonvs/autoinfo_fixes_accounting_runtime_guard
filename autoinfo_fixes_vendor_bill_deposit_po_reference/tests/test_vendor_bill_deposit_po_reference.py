from lxml import etree

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestVendorBillDepositPOReference(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.move_model = cls.env["account.move"]

    def test_account_move_exposes_deposit_po_ref_field(self):
        field = self.move_model._fields.get("deposit_po_ref")
        self.assertTrue(
            field,
            "account.move should expose deposit_po_ref so vendor bills can store a purchase order reference.",
        )
        self.assertEqual(
            field.comodel_name,
            "purchase.order",
            "deposit_po_ref should link to purchase.order.",
        )
        self.assertEqual(
            field.string,
            "PO Reference",
            "deposit_po_ref should use the PO Reference label.",
        )

    def test_form_view_contains_vendor_bill_po_reference_field(self):
        result = self.move_model.fields_view_get(view_type="form")
        self.assertIn(
            "deposit_po_ref",
            result["fields"],
            "The form view metadata should expose deposit_po_ref.",
        )

        doc = etree.fromstring(result["arch"].encode())
        po_fields = doc.xpath("//field[@name='deposit_po_ref']")
        self.assertTrue(
            po_fields,
            "The account.move form should render deposit_po_ref for vendor bill deposit payments.",
        )
        attrs = po_fields[0].get("attrs", "")
        self.assertIn("deposit_payment", attrs)
        self.assertIn("move_type", attrs)
        self.assertIn("in_invoice", attrs)

    def test_form_view_keeps_sale_side_so_reference(self):
        result = self.move_model.fields_view_get(view_type="form")
        doc = etree.fromstring(result["arch"].encode())

        so_fields = doc.xpath("//field[@name='deposit_so_ref']")
        self.assertTrue(
            so_fields,
            "The account.move form should still render deposit_so_ref for the sales flow.",
        )
        attrs = so_fields[-1].get("attrs", "")
        self.assertIn("deposit_payment", attrs)
        self.assertIn("move_type", attrs)
        self.assertIn("out_invoice", attrs)
