# Vendor Bill Deposit PO Reference Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and extend a separate Odoo 15 addon that shows `PO Reference` on `Vendor Bill`, keeps `SO Reference` on customer invoices, filters both dropdowns, and syncs source-document/header-line links without creating new lines.

**Architecture:** Extend the existing overlay addon `autoinfo_fixes_vendor_bill_deposit_po_reference` in two layers. First, keep the current UI layer that shows `deposit_po_ref`, keeps `deposit_so_ref`, and filters both dropdowns by partner and confirmed state. Second, add a model-level `onchange` synchronization layer that writes the same source-document fields the legacy purchase/sales wizards use (`po_origin`, `origin_second`, `purchase_line_id`, `vendor_source_doc`, `sale_line_ids`) onto the current draft move and its existing lines by matching `product_id` in order, while never creating or deleting lines.

**Tech Stack:** Odoo 15 CE, Python, XML inherited views, `account.move`, `purchase.order`, `sale.order`, Odoo transactional tests, `lxml.etree`

---

## File Map

- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\account_move.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\views\account_move_view.xml`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\README.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\user_guide.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\technical_guide.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\troubleshooting.md`
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\account_move.py`
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`

## Test Command Baseline

Use this command whenever a step says to run the module tests:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected success signal:

```text
... autoinfo_fixes_vendor_bill_deposit_po_reference ... OK
```

## Upgrade Command Baseline

Use this command to verify the addon upgrades cleanly after code changes:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
```

Expected success signal:

```text
Module autoinfo_fixes_vendor_bill_deposit_po_reference upgraded without Python, XML, or dependency errors
```

### Task 1: Scaffold The Overlay Addon

**Files:**
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\__init__.py`

- [ ] **Step 1: Create the addon entry files**

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__init__.py
from . import models
```

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py
# import models here in Task 3
```

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\__init__.py
# import tests here in Task 2
```

- [ ] **Step 2: Create the manifest with isolated dependencies**

```python
{
    "name": "AUTO-INFO : Vendor Bill Deposit PO Reference Fix",
    "version": "15.0.1.0.0",
    "summary": "Show PO Reference on vendor bill deposit payment without changing the deposit flow",
    "author": "The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon",
    "license": "LGPL-3",
    "category": "Accounting",
    "depends": [
        "account",
        "purchase",
        "dtr_customer_invoices",
        "dtr_deposit_payment",
        "autoinfo_accounting_form",
    ],
    "data": [],
    "installable": True,
    "application": False,
}
```

- [ ] **Step 3: Install the empty scaffold once to verify imports and dependencies**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
```

Expected:

```text
Module autoinfo_fixes_vendor_bill_deposit_po_reference loads successfully with no import or dependency errors
```

- [ ] **Step 4: Commit the scaffold**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__init__.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\__init__.py
git commit -m "build: scaffold vendor bill deposit po reference overlay"
```

### Task 2: Write The Failing Regression Tests (Domain Filtering)

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`
- Read for view-test pattern: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_hr_expense_duplicate_guard\tests\test_expense_duplicate_guard.py`

- [ ] **Step 1: Add failing tests for partner + confirmed-state domains**

Patch:

```python
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
        doc = etree.fromstring(result["arch"].encode())
        po_fields = doc.xpath("//field[@name='deposit_po_ref']")
        self.assertTrue(po_fields)
        domain = po_fields[0].get("domain", "")
        self.assertIn("partner_id", domain)
        self.assertIn("state", domain)
        self.assertIn("purchase", domain)
        self.assertIn("done", domain)

    def test_form_view_keeps_sale_side_so_reference(self):
        result = self.move_model.fields_view_get(view_type="form")
        doc = etree.fromstring(result["arch"].encode())
        so_fields = doc.xpath("//field[@name='deposit_so_ref']")
        self.assertTrue(so_fields)
        domain = so_fields[-1].get("domain", "")
        self.assertIn("partner_id", domain)
        self.assertIn("state", domain)
        self.assertIn("sale", domain)
        self.assertIn("done", domain)
```

- [ ] **Step 2: Run the tests to verify they fail before implementation**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
FAIL: the view domains do not yet restrict records to the same partner and confirmed states
```

- [ ] **Step 3: Commit the failing tests**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py
git commit -m "test: enforce deposit reference domain filtering"
```

### Task 3: Implement Domain Filtering In The Overlay View

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\views\account_move_view.xml`
- Test: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`

- [ ] **Step 1: Add the minimal domains for partner + confirmed state**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="autoinfo_fixes_vendor_bill_deposit_po_reference_form" model="ir.ui.view">
            <field name="name">autoinfo.fixes.vendor.bill.deposit.po.reference.form</field>
            <field name="model">account.move</field>
            <field name="inherit_id" ref="autoinfo_accounting_form.autoinfo_accounting_form_inherit_dtr_view_move_form" />
            <field name="arch" type="xml">
                <xpath expr="//field[@name='deposit_so_ref']" position="attributes">
                    <attribute name="attrs">{'invisible': ['|', ('order_type', '!=', 'deposit_payment'), ('move_type', '!=', 'out_invoice')]}</attribute>
                    <attribute name="domain">[('partner_id', '=', partner_id), ('state', 'in', ['sale', 'done'])]</attribute>
                </xpath>
                <xpath expr="//field[@name='deposit_so_ref']" position="after">
                    <field name="deposit_po_ref" domain="[('partner_id', '=', partner_id), ('state', 'in', ['purchase', 'done'])]" attrs="{'invisible': ['|', ('order_type', '!=', 'deposit_payment'), ('move_type', '!=', 'in_invoice')]}"/>
                </xpath>
            </field>
        </record>
    </data>
</odoo>
```

- [ ] **Step 2: Run the focused regression tests**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
PASS: all tests in test_vendor_bill_deposit_po_reference.py succeed
```

- [ ] **Step 3: Run one upgrade pass to validate XML loading**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
```

Expected:

```text
No ParseError, FieldError, or dependency error during module upgrade
```

- [ ] **Step 4: Commit the implementation**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\views\account_move_view.xml
git commit -m "feat: filter deposit reference dropdowns by partner and state"
```

### Task 4: Add Minimal Module Documentation

**Files:**
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\README.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\user_guide.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\technical_guide.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\troubleshooting.md`

- [ ] **Step 1: Write a short README for module purpose and scope**

```markdown
# AUTO-INFO : Vendor Bill Deposit PO Reference Fix

## Purpose
- Show `PO Reference` on `Vendor Bill` when `Type = Deposit Payment`
- Keep `SO Reference` on customer invoice
- Do not change deposit wizard logic

## Scope
- Overlay addon only
- No report changes
- No migration required

## Credits
- The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon
- AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT
```

- [ ] **Step 2: Write the user guide in simple Thai**

```markdown
# คู่มือผู้ใช้

## ใช้งานเมื่อไร
- ใช้ตอนสร้าง `Vendor Bill`
- และเลือก `Type = Deposit Payment`

## วิธีใช้
1. เปิดเอกสาร `Vendor Bill`
2. เลือก `Type = Deposit Payment`
3. ระบบจะแสดงช่อง `PO Reference`
4. เลือกใบสั่งซื้อที่ต้องการอ้างอิง
5. ใช้งานปุ่ม deposit เดิมได้ตามปกติ

## หมายเหตุ
- ฝั่ง `Customer Invoice` ยังใช้ `SO Reference` เหมือนเดิม
```

- [ ] **Step 3: Write the technical guide**

```markdown
# คู่มือเทคนิค

## โครงสร้าง
- โมดูลนี้เป็น overlay addon
- inherit `account.move`
- เพิ่มฟิลด์ `deposit_po_ref`
- inherit view จาก `autoinfo_accounting_form`

## จุดสำคัญ
- ไม่แก้ logic ใน `dtr_deposit_payment`
- ไม่แก้รายงานที่ใช้ `deposit_so_ref`
- ใช้การแยก field ตาม `move_type`

## Dependency
- `account`
- `purchase`
- `dtr_customer_invoices`
- `dtr_deposit_payment`
- `autoinfo_accounting_form`
```

- [ ] **Step 4: Write the troubleshooting guide**

```markdown
# การแก้ปัญหา

## ไม่เห็นช่อง PO Reference
- ตรวจว่าเอกสารเป็น `Vendor Bill`
- ตรวจว่า `Type` เป็น `Deposit Payment`
- ตรวจว่าโมดูลเสริมติดตั้งแล้ว

## อัปเกรดโมดูลไม่ผ่าน
- ตรวจ dependency ใน `addons-path`
- ตรวจว่า `autoinfo_accounting_form` และ `dtr_deposit_payment` โหลดได้
- ตรวจ syntax ของไฟล์ XML และ Python

## ช่องเดิม SO Reference ยังแสดงผิดฝั่ง
- ตรวจว่ามีการอัปเกรดโมดูลเสริมล่าสุดแล้ว
- ตรวจลำดับ inherited view ในฐานข้อมูล
```

- [ ] **Step 5: Commit the docs**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\README.md c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\user_guide.md c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\technical_guide.md c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\docs\troubleshooting.md
git commit -m "docs: add vendor bill deposit po reference guides"
```

### Task 5: Final Verification And Packaging Notes

**Files:**
- Test: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`
- Review: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py`
- Review: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\views\account_move_view.xml`

- [ ] **Step 1: Run the full module test command again**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
OK: regression tests pass after docs and final file cleanup
```

- [ ] **Step 2: Run a manual smoke-upgrade on the target database**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d <target_database> -u autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
```

Expected:

```text
The target database upgrades cleanly and the new field appears on vendor bill deposit payment forms
```

- [ ] **Step 3: Perform the UI smoke test**

Checklist:

```text
1. Open Customer Invoice + Type = Deposit Payment -> SO Reference is visible
2. Open Vendor Bill + Type = Deposit Payment -> PO Reference is visible
3. Open Vendor Bill + Type != Deposit Payment -> PO Reference is hidden
4. Click Add Deposit Payment -> existing wizard still opens
```

- [ ] **Step 4: Commit the verification-ready state**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference
git commit -m "chore: finalize vendor bill deposit po reference overlay"
```

### Task 6: Write The Failing Sync Tests

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`

- [ ] **Step 1: Add failing tests for header sync and line linkage**

```python
    def test_onchange_deposit_po_ref_updates_vendor_header_and_line_links(self):
        vendor = self.env["res.partner"].create({"name": "Vendor Sync"})
        product = self.env["product.product"].create({"name": "Sync Product", "type": "consu"})
        po = self.env["purchase.order"].create({"partner_id": vendor.id})
        po_line = self.env["purchase.order.line"].create({
            "order_id": po.id,
            "name": "Sync Product",
            "product_id": product.id,
            "product_qty": 1.0,
            "price_unit": 100.0,
            "date_planned": fields.Datetime.now(),
            "product_uom": product.uom_po_id.id or product.uom_id.id,
        })
        po.button_confirm()

        bill = self.env["account.move"].new({
            "move_type": "in_invoice",
            "partner_id": vendor.id,
            "order_type": "deposit_payment",
            "invoice_line_ids": [Command.create({
                "name": "Sync Product",
                "product_id": product.id,
                "quantity": 1.0,
                "price_unit": 100.0,
            })],
        })
        bill.deposit_po_ref = po
        bill._onchange_deposit_po_ref_sync_links()

        self.assertEqual(bill.po_origin, po.name)
        self.assertEqual(bill.invoice_line_ids[0].purchase_line_id, po_line)
        self.assertEqual(bill.invoice_line_ids[0].vendor_source_doc, po.name)

    def test_onchange_deposit_so_ref_updates_customer_header_and_line_links(self):
        customer = self.env["res.partner"].create({"name": "Customer Sync"})
        product = self.env["product.product"].create({"name": "SO Sync Product", "type": "consu"})
        order = self.env["sale.order"].create({"partner_id": customer.id})
        order_line = self.env["sale.order.line"].create({
            "order_id": order.id,
            "name": "SO Sync Product",
            "product_id": product.id,
            "product_uom_qty": 1.0,
            "price_unit": 100.0,
        })
        order.action_confirm()

        invoice = self.env["account.move"].new({
            "move_type": "out_invoice",
            "partner_id": customer.id,
            "order_type": "deposit_payment",
            "invoice_line_ids": [Command.create({
                "name": "SO Sync Product",
                "product_id": product.id,
                "quantity": 1.0,
                "price_unit": 100.0,
            })],
        })
        invoice.deposit_so_ref = order
        invoice._onchange_deposit_so_ref_sync_links()

        self.assertEqual(invoice.origin_second, order.name)
        self.assertEqual(invoice.invoice_line_ids[0].sale_line_ids, order_line)

    def test_onchange_sync_skips_non_matching_lines_without_creating_new_ones(self):
        vendor = self.env["res.partner"].create({"name": "Vendor No Match"})
        po = self.env["purchase.order"].create({"partner_id": vendor.id})
        other_product = self.env["product.product"].create({"name": "Other Product", "type": "consu"})
        self.env["purchase.order.line"].create({
            "order_id": po.id,
            "name": "Other Product",
            "product_id": other_product.id,
            "product_qty": 1.0,
            "price_unit": 50.0,
            "date_planned": fields.Datetime.now(),
            "product_uom": other_product.uom_po_id.id or other_product.uom_id.id,
        })
        po.button_confirm()

        unmatched_product = self.env["product.product"].create({"name": "Unmatched Product", "type": "consu"})
        bill = self.env["account.move"].new({
            "move_type": "in_invoice",
            "partner_id": vendor.id,
            "order_type": "deposit_payment",
            "invoice_line_ids": [Command.create({
                "name": "Unmatched Product",
                "product_id": unmatched_product.id,
                "quantity": 1.0,
                "price_unit": 50.0,
            })],
        })
        original_line_count = len(bill.invoice_line_ids)
        bill.deposit_po_ref = po
        bill._onchange_deposit_po_ref_sync_links()

        self.assertEqual(len(bill.invoice_line_ids), original_line_count)
        self.assertFalse(bill.invoice_line_ids[0].purchase_line_id)
        self.assertFalse(bill.invoice_line_ids[0].vendor_source_doc)
```

- [ ] **Step 2: Run the tests to verify they fail before implementation**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
FAIL: account.move does not yet expose onchange sync methods and existing lines are not yet linked from the chosen PO/SO
```

- [ ] **Step 3: Commit the failing sync tests**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py
git commit -m "test: add deposit reference sync regressions"
```

### Task 7: Implement Header And Line Sync

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\account_move.py`
- Test: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`

- [ ] **Step 1: Add helper methods for matching existing lines by product in order**

```python
from collections import defaultdict

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    deposit_po_ref = fields.Many2one("purchase.order", string="PO Reference")

    def _match_existing_lines_by_product(self, source_lines, target_lines):
        buckets = defaultdict(list)
        for line in source_lines:
            if line.product_id:
                buckets[line.product_id.id].append(line)

        matches = {}
        for target in target_lines.filtered(lambda line: not line.display_type and line.product_id):
            bucket = buckets.get(target.product_id.id, [])
            matches[target] = bucket.pop(0) if bucket else False
        return matches
```

- [ ] **Step 2: Implement vendor-bill onchange sync without creating new lines**

```python
    @api.onchange("deposit_po_ref")
    def _onchange_deposit_po_ref_sync_links(self):
        for move in self:
            if move.move_type != "in_invoice" or move.order_type != "deposit_payment" or not move.deposit_po_ref:
                continue

            po = move.deposit_po_ref
            if "po_origin" in move._fields:
                move.po_origin = po.name
            if "invoice_origin" in move._fields:
                move.invoice_origin = po.name

            source_lines = po.order_line.filtered(lambda line: line.product_id)
            matches = move._match_existing_lines_by_product(source_lines, move.invoice_line_ids)
            for target_line, source_line in matches.items():
                if not source_line:
                    continue
                if "purchase_line_id" in target_line._fields:
                    target_line.purchase_line_id = source_line
                if "vendor_source_doc" in target_line._fields:
                    target_line.vendor_source_doc = source_line.order_id.name
```

- [ ] **Step 3: Implement customer-invoice onchange sync without creating new lines**

```python
    @api.onchange("deposit_so_ref")
    def _onchange_deposit_so_ref_sync_links(self):
        for move in self:
            if move.move_type != "out_invoice" or move.order_type != "deposit_payment" or not move.deposit_so_ref:
                continue

            so = move.deposit_so_ref
            if "origin_second" in move._fields:
                move.origin_second = so.name
            elif "invoice_origin" in move._fields:
                move.invoice_origin = so.name

            source_lines = so.order_line.filtered(lambda line: line.product_id)
            matches = move._match_existing_lines_by_product(source_lines, move.invoice_line_ids)
            for target_line, source_line in matches.items():
                if not source_line:
                    continue
                if "sale_line_ids" in target_line._fields:
                    target_line.sale_line_ids = [(6, 0, source_line.ids)]
```

- [ ] **Step 4: Run the focused regression tests**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
PASS: header sync and line linkage tests succeed without creating new lines
```

- [ ] **Step 5: Run one upgrade pass to validate model loading**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_apps_oca_account_invoicing,c:\odoo\addons_autoinfo\odoo15_apps_oca_server_ux,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
```

Expected:

```text
No ParseError, FieldError, or onchange-related error during module upgrade
```

- [ ] **Step 6: Commit the sync implementation**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\account_move.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py
git commit -m "feat: sync deposit references to source fields and line links"
```
