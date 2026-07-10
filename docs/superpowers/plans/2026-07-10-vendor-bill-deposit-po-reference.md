# Vendor Bill Deposit PO Reference Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a separate Odoo 15 addon that shows `PO Reference` on `Vendor Bill` when `Type = Deposit Payment`, while preserving the existing deposit flow and the existing `SO Reference` on customer invoices.

**Architecture:** Create a small overlay addon named `autoinfo_fixes_vendor_bill_deposit_po_reference` that inherits `account.move`, adds one new `purchase.order` reference field, and overrides the existing accounting form view from `autoinfo_accounting_form` so the sale-side field and purchase-side field are shown in different document types. Keep the change isolated to UI and metadata only; do not touch the deposit wizard logic in `dtr_deposit_payment` and do not alter existing reports.

**Tech Stack:** Odoo 15 CE, Python, XML inherited views, `account.move`, `purchase.order`, Odoo transactional tests, `lxml.etree`

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

## Test Command Baseline

Use this command whenever a step says to run the module tests:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected success signal:

```text
... autoinfo_fixes_vendor_bill_deposit_po_reference ... OK
```

## Upgrade Command Baseline

Use this command to verify the addon upgrades cleanly after code changes:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
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

### Task 2: Write The Failing Regression Tests

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`
- Read for view-test pattern: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_hr_expense_duplicate_guard\tests\test_expense_duplicate_guard.py`

- [ ] **Step 1: Wire the tests package and create failing tests for the new field and split visibility**

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\__init__.py
from . import test_vendor_bill_deposit_po_reference
```

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py
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
```

- [ ] **Step 2: Run the tests to verify they fail before implementation**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
FAIL: deposit_po_ref does not exist yet, and the inherited form view does not yet split SO Reference and PO Reference by move_type
```

- [ ] **Step 3: Commit the failing tests**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py
git commit -m "test: add vendor bill deposit po reference regressions"
```

### Task 3: Implement The Overlay Model And View

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py`
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\account_move.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\views\account_move_view.xml`
- Test: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\tests\test_vendor_bill_deposit_po_reference.py`

- [ ] **Step 1: Wire the model package and manifest to load the implementation**

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py
from . import account_move
```

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py
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
    "data": [
        "views/account_move_view.xml",
    ],
    "installable": True,
    "application": False,
}
```

- [ ] **Step 2: Add the minimal model field**

```python
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    deposit_po_ref = fields.Many2one("purchase.order", string="PO Reference")
```

- [ ] **Step 3: Override the inherited form view without touching the original addon**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="view_move_form_vendor_bill_deposit_po_reference" model="ir.ui.view">
            <field name="name">account.move.form.vendor.bill.deposit.po.reference</field>
            <field name="model">account.move</field>
            <field name="inherit_id" ref="autoinfo_accounting_form.autoinfo_accounting_form_inherit_dtr_view_move_form"/>
            <field name="arch" type="xml">
                <field name="deposit_so_ref" position="replace">
                    <field
                        name="deposit_so_ref"
                        domain="[('state', 'in', ['done'])]"
                        attrs="{'invisible': ['|', ('order_type', '!=', 'deposit_payment'), ('move_type', '!=', 'out_invoice')]}"
                    />
                    <field
                        name="deposit_po_ref"
                        domain="[('partner_id', '=', partner_id)]"
                        attrs="{'invisible': ['|', ('order_type', '!=', 'deposit_payment'), ('move_type', '!=', 'in_invoice')]}"
                    />
                </field>
            </field>
        </record>
    </data>
</odoo>
```

- [ ] **Step 4: Run the focused regression tests**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -i autoinfo_fixes_vendor_bill_deposit_po_reference --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_fixes_vendor_bill_deposit_po_reference
```

Expected:

```text
PASS: all tests in test_vendor_bill_deposit_po_reference.py succeed
```

- [ ] **Step 5: Run one upgrade pass to validate XML loading**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_accounting,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_vendor_bill_deposit_po_reference -u autoinfo_fixes_vendor_bill_deposit_po_reference --stop-after-init
```

Expected:

```text
No ParseError, FieldError, or dependency error during module upgrade
```

- [ ] **Step 6: Commit the implementation**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\__manifest__.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\__init__.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\models\account_move.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_fixes_vendor_bill_deposit_po_reference\views\account_move_view.xml
git commit -m "feat: add po reference overlay for vendor bill deposit payment"
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
