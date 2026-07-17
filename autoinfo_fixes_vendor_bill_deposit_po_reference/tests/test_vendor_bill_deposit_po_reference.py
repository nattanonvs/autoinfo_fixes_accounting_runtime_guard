from lxml import etree

from odoo import Command, fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestVendorBillDepositPOReference(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.move_model = cls.env["account.move"]
        cls.company = cls.env.company
        cls.receivable_account = cls._get_account(
            "account.data_account_type_receivable",
            "TVBDPR",
            "Test Vendor Bill Deposit Receivable",
            reconcile=True,
        )
        cls.payable_account = cls._get_account(
            "account.data_account_type_payable",
            "TVBDPP",
            "Test Vendor Bill Deposit Payable",
            reconcile=True,
        )
        cls.expense_account = cls._get_account(
            "account.data_account_type_expenses",
            "TVBDPE",
            "Test Vendor Bill Deposit Expense",
        )
        cls.income_account = cls._get_account(
            "account.data_account_type_revenue",
            "TVBDPI",
            "Test Vendor Bill Deposit Income",
        )
        cls.purchase_journal = cls._get_journal(
            "purchase",
            "TVBPJ",
            "Test Vendor Bill Deposit Purchase Journal",
        )
        cls.sale_journal = cls._get_journal(
            "sale",
            "TVBSJ",
            "Test Vendor Bill Deposit Sale Journal",
        )
        cls.pricelist = cls.env["product.pricelist"].search(
            [("company_id", "in", [False, cls.company.id])],
            limit=1,
        )
        if not cls.pricelist:
            cls.pricelist = cls.env["product.pricelist"].create(
                {
                    "name": "Test Vendor Bill Deposit Pricelist",
                    "currency_id": cls.company.currency_id.id,
                    "company_id": cls.company.id,
                }
            )

    @classmethod
    def _get_account(cls, account_type_xmlid, code, name, reconcile=False):
        account_type = cls.env.ref(account_type_xmlid)
        account = cls.env["account.account"].search(
            [
                ("company_id", "=", cls.company.id),
                ("user_type_id", "=", account_type.id),
            ],
            limit=1,
        )
        if account:
            return account
        return cls.env["account.account"].create(
            {
                "name": name,
                "code": code,
                "user_type_id": account_type.id,
                "reconcile": reconcile,
                "company_id": cls.company.id,
            }
        )

    @classmethod
    def _get_journal(cls, journal_type, code, name):
        journal = cls.env["account.journal"].search(
            [("type", "=", journal_type), ("company_id", "=", cls.company.id)],
            limit=1,
        )
        if journal:
            return journal
        return cls.env["account.journal"].create(
            {
                "name": name,
                "code": code,
                "type": journal_type,
                "company_id": cls.company.id,
            }
        )

    def _normalize_domain(self, domain):
        return (domain or "").replace(" ", "")

    def _create_partner(self, name, customer=False, supplier=False):
        return self.env["res.partner"].create(
            {
                "name": name,
                "customer_rank": 1 if customer else 0,
                "supplier_rank": 1 if supplier else 0,
                "property_account_receivable_id": self.receivable_account.id,
                "property_account_payable_id": self.payable_account.id,
                "company_id": self.company.id,
            }
        )

    def _create_product(self, name):
        return self.env["product.product"].create(
            {
                "name": name,
                "type": "consu",
                "list_price": 100.0,
                "standard_price": 50.0,
                "property_account_income_id": self.income_account.id,
                "property_account_expense_id": self.expense_account.id,
                "company_id": self.company.id,
            }
        )

    def _create_purchase_order(self, vendor, product, name):
        purchase_order = self.env["purchase.order"].create(
            {
                "name": name,
                "partner_id": vendor.id,
                "company_id": self.company.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": product.display_name,
                            "product_id": product.id,
                            "product_qty": 1.0,
                            "product_uom": product.uom_po_id.id,
                            "price_unit": 100.0,
                            "date_planned": fields.Datetime.now(),
                        },
                    )
                ],
            }
        )
        purchase_order.button_confirm()
        return purchase_order, purchase_order.order_line[:1]

    def _create_sale_order(self, customer, product, name):
        sale_order = self.env["sale.order"].create(
            {
                "name": name,
                "partner_id": customer.id,
                "partner_invoice_id": customer.id,
                "partner_shipping_id": customer.id,
                "pricelist_id": self.pricelist.id,
                "company_id": self.company.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": product.display_name,
                            "product_id": product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        return sale_order, sale_order.order_line[:1]

    def _new_vendor_bill(self, vendor, product):
        return self.move_model.with_context(
            default_move_type="in_invoice",
            default_journal_id=self.purchase_journal.id,
        ).new(
            {
                "move_type": "in_invoice",
                "partner_id": vendor.id,
                "journal_id": self.purchase_journal.id,
                "order_type": "deposit_payment",
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": product.display_name,
                            "product_id": product.id,
                            "quantity": 1.0,
                            "price_unit": 100.0,
                            "account_id": self.expense_account.id,
                        }
                    )
                ],
            }
        )

    def _new_customer_invoice(self, customer, product):
        return self.move_model.with_context(
            default_move_type="out_invoice",
            default_journal_id=self.sale_journal.id,
        ).new(
            {
                "move_type": "out_invoice",
                "partner_id": customer.id,
                "journal_id": self.sale_journal.id,
                "order_type": "deposit_payment",
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": product.display_name,
                            "product_id": product.id,
                            "quantity": 1.0,
                            "price_unit": 100.0,
                            "account_id": self.income_account.id,
                        }
                    )
                ],
            }
        )

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
        domain = self._normalize_domain(po_fields[0].get("domain"))
        self.assertTrue(domain, "deposit_po_ref should define a domain for dropdown filtering.")
        self.assertIn("partner_id", domain)
        self.assertIn("state", domain)
        self.assertIn("'purchase'", domain)
        self.assertIn("'done'", domain)
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
        domain = self._normalize_domain(so_fields[-1].get("domain"))
        self.assertTrue(domain, "deposit_so_ref should define a domain for dropdown filtering.")
        self.assertIn("partner_id", domain)
        self.assertIn("state", domain)
        self.assertIn("'sale'", domain)
        self.assertIn("'done'", domain)
        attrs = so_fields[-1].get("attrs", "")
        self.assertIn("deposit_payment", attrs)
        self.assertIn("move_type", attrs)
        self.assertIn("out_invoice", attrs)

    def test_onchange_deposit_po_ref_syncs_vendor_header_and_existing_line_links(self):
        vendor = self._create_partner("Vendor Deposit Sync", supplier=True)
        product = self._create_product("Vendor Deposit Sync Product")
        purchase_order, purchase_line = self._create_purchase_order(
            vendor,
            product,
            "PO-DEPOSIT-SYNC-01",
        )
        bill = self._new_vendor_bill(vendor, product)

        bill.deposit_po_ref = purchase_order
        bill._onchange_deposit_po_ref_sync_links()

        self.assertEqual(
            bill.po_origin,
            purchase_order.name,
            "Selecting deposit_po_ref should sync the vendor-bill source header from the chosen purchase order.",
        )
        self.assertEqual(
            bill.invoice_line_ids.purchase_line_id,
            purchase_line,
            "Selecting deposit_po_ref should reuse the existing invoice line and attach the matching purchase_line_id.",
        )
        self.assertEqual(
            bill.invoice_line_ids.vendor_source_doc,
            purchase_order.name,
            "Selecting deposit_po_ref should sync vendor_source_doc onto the existing invoice line.",
        )

    def test_onchange_deposit_so_ref_syncs_customer_header_and_existing_line_links(self):
        customer = self._create_partner("Customer Deposit Sync", customer=True)
        product = self._create_product("Customer Deposit Sync Product")
        sale_order, sale_line = self._create_sale_order(
            customer,
            product,
            "SO-DEPOSIT-SYNC-01",
        )
        invoice = self._new_customer_invoice(customer, product)

        invoice.deposit_so_ref = sale_order
        invoice._onchange_deposit_so_ref_sync_links()

        self.assertEqual(
            invoice.origin_second,
            sale_order.name,
            "Selecting deposit_so_ref should sync the sales-side source header from the chosen sale order.",
        )
        self.assertEqual(
            invoice.invoice_line_ids.sale_line_ids.ids,
            sale_line.ids,
            "Selecting deposit_so_ref should reuse the existing invoice line and attach the matching sale_line_ids.",
        )

    def test_onchange_sync_skips_unmatched_lines_without_creating_new_ones(self):
        vendor = self._create_partner("Vendor Deposit No Match", supplier=True)
        source_product = self._create_product("Vendor Deposit Source Product")
        unmatched_product = self._create_product("Vendor Deposit Unmatched Product")
        purchase_order, _purchase_line = self._create_purchase_order(
            vendor,
            source_product,
            "PO-DEPOSIT-SYNC-UNMATCHED",
        )
        bill = self._new_vendor_bill(vendor, unmatched_product)
        original_line_count = len(bill.invoice_line_ids)

        bill.deposit_po_ref = purchase_order
        bill._onchange_deposit_po_ref_sync_links()

        self.assertEqual(
            len(bill.invoice_line_ids),
            original_line_count,
            "Selecting deposit_po_ref should not create extra invoice lines when no existing line matches the PO product.",
        )
        self.assertFalse(
            bill.invoice_line_ids.purchase_line_id,
            "Unmatched lines should remain unlinked instead of being rebound to a different purchase line.",
        )
        self.assertFalse(
            bill.invoice_line_ids.vendor_source_doc,
            "Unmatched lines should keep vendor_source_doc empty instead of fabricating a new source link.",
        )
