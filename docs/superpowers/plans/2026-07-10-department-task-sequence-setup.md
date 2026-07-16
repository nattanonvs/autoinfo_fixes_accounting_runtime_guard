# Department Task Sequence Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let users configure, create, refresh, and select task sequences from `Department` without visiting `Technical > Sequences`, while preserving task code generation by creator department and the `[CODE/JOB NO] ชื่องาน` display format.

**Architecture:** Extend the existing `autoinfo_project` addon in place. Put all sequence setup UX on `hr.department`, keep `ir.sequence` as the backend engine, and keep `project.task` focused on consuming the department-selected sequence plus clear Department-first error messages. Add transactional tests that cover setup, validation, and code generation.

**Tech Stack:** Odoo 15 CE, Python, XML inherited views, `hr.department`, `ir.sequence`, `project.task`, Odoo `TransactionCase`, `lxml.etree`

---

## File Map

- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\models\hr_department.py`
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml`
- Modify: `c:\odoo\addons_autoinfo\odoo15_mods\dtr_project\models\project_task.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`
- Read during implementation: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\__manifest__.py`

## Test Command Baseline

Use this command whenever a step says to run the module tests:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -i autoinfo_project,dtr_project --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_project
```

Expected success signal:

```text
... autoinfo_project ... OK
```

## Upgrade Command Baseline

Use this command to verify the addon upgrades cleanly after code changes:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --stop-after-init
```

Expected success signal:

```text
Modules autoinfo_project and dtr_project upgrade without Python, XML, or dependency errors
```

### Task 1: Add Regression Tests For Department Sequence Setup

**Files:**
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\__init__.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`

- [ ] **Step 1: Create the tests package entrypoint**

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\__init__.py
from . import test_department_task_sequence_setup
```

- [ ] **Step 2: Write failing tests for Department actions, status, and task code generation**

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py
from lxml import etree

from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestDepartmentTaskSequenceSetup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department_model = cls.env["hr.department"]
        cls.sequence_model = cls.env["ir.sequence"]
        cls.user_model = cls.env["res.users"]
        cls.employee_model = cls.env["hr.employee"]
        cls.task_model = cls.env["project.task"]
        cls.project_model = cls.env["project.project"]
        cls.category_model = cls.env["project.task.category"]
        cls.site_model = cls.env["project.site"]
        cls.db_model = cls.env["project.site.database"]

        cls.department = cls.department_model.create({
            "name": "Business Analyst",
            "task_code_prefix": "BA",
        })
        cls.user = cls.user_model.create({
            "name": "BA User",
            "login": "ba_user_sequence_setup",
            "email": "ba_user_sequence_setup@example.com",
        })
        cls.employee_model.create({
            "name": "BA User",
            "user_id": cls.user.id,
            "department_id": cls.department.id,
        })

        cls.project = cls.project_model.create({
            "name": "Project BA",
            "job_type": "job",
            "project_department_id": cls.department.id,
            "job_no": "JOB-BA-0001",
        })
        cls.category = cls.category_model.create({"name": "Implementation"})
        cls.site = cls.site_model.create({
            "name": "https://example.test",
            "project_id": cls.project.id,
        })
        cls.database = cls.db_model.create({
            "name": "TESTDB",
            "project_site_id": cls.site.id,
        })

    def test_action_create_task_sequence_builds_monthly_sequence(self):
        self.department.action_create_task_sequence()
        sequence = self.department.project_task_sequence_id

        self.assertTrue(sequence, "Department should receive a generated task sequence.")
        self.assertEqual(sequence.padding, 5)
        self.assertTrue(sequence.use_date_range)
        self.assertEqual(sequence.prefix, "BA%(range_month)s%(range_y)s-")

    def test_sequence_status_marks_ready_after_generation(self):
        self.department.action_create_task_sequence()
        self.department.invalidate_cache()

        self.assertEqual(
            self.department.task_sequence_status,
            "ready",
            "Department should show ready after a valid task sequence is linked.",
        )
        self.assertTrue(
            self.department.task_sequence_preview.startswith("BA"),
            "Preview should show the department prefix at the start.",
        )

    def test_task_creation_uses_department_selected_sequence(self):
        self.department.action_create_task_sequence()

        task = self.task_model.with_user(self.user).create({
            "name": "Create BA task",
            "project_id": self.project.id,
            "task_category_id": self.category.id,
            "project_site_id": self.site.id,
            "project_site_database_ids": [(6, 0, [self.database.id])],
            "user_id": self.user.id,
        })

        self.assertRegex(task.code, r"^BA\d{4}-\d{5}$")
        self.assertEqual(
            task.display_name,
            "[%s/%s] %s" % (task.code, self.project.job_no, task.name),
        )

    def test_task_creation_explains_department_setup_when_sequence_missing(self):
        with self.assertRaises(ValidationError):
            self.task_model.with_user(self.user).create({
                "name": "Task without setup",
                "project_id": self.project.id,
                "task_category_id": self.category.id,
                "project_site_id": self.site.id,
                "project_site_database_ids": [(6, 0, [self.database.id])],
                "user_id": self.user.id,
            })

    def test_department_form_exposes_setup_buttons_and_fields(self):
        result = self.department_model.fields_view_get(view_type="form")
        doc = etree.fromstring(result["arch"].encode())

        self.assertTrue(doc.xpath("//field[@name='task_code_prefix']"))
        self.assertTrue(doc.xpath("//field[@name='project_task_sequence_id']"))
        self.assertTrue(doc.xpath("//field[@name='task_sequence_status']"))
        self.assertTrue(doc.xpath("//field[@name='task_sequence_preview']"))
        self.assertTrue(doc.xpath("//button[@name='action_create_task_sequence']"))
        self.assertTrue(doc.xpath("//button[@name='action_refresh_task_sequence']"))
```

- [ ] **Step 3: Run the tests to confirm the new behavior is not implemented yet**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -i autoinfo_project,dtr_project --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_project
```

Expected:

```text
FAIL: hr.department is missing the sequence setup actions, computed status/preview fields, and the form view controls
```

- [ ] **Step 4: Commit the failing tests**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\__init__.py c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py
git commit -m "test: add department task sequence setup regression coverage"
```

### Task 2: Implement Department Setup Actions And Validation

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\models\hr_department.py`
- Read: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`

- [ ] **Step 1: Add computed status/preview fields and shared validation helpers**

```python
# c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\models\hr_department.py
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrDepartment(models.Model):
    _inherit = "hr.department"

    task_code_prefix = fields.Char(string="Task Code Prefix")
    project_no_job_sequence_id = fields.Many2one("ir.sequence", string="Project Job No.(Job) Sequence", check_company=True)
    project_no_pm_sequence_id = fields.Many2one("ir.sequence", string="Project Job No.(PM) Sequence", check_company=True)
    project_no_service_sequence_id = fields.Many2one("ir.sequence", string="Project Job No.(Service) Sequence", check_company=True)
    project_task_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Task Sequence",
        check_company=True,
        domain="[('active', '=', True)]",
    )
    task_sequence_status = fields.Selection(
        [
            ("not_configured", "Not Configured"),
            ("invalid", "Invalid Setup"),
            ("ready", "Ready"),
        ],
        string="Task Sequence Status",
        compute="_compute_task_sequence_setup",
    )
    task_sequence_preview = fields.Char(
        string="Task Sequence Preview",
        compute="_compute_task_sequence_setup",
    )

    @api.depends(
        "task_code_prefix",
        "project_task_sequence_id",
        "project_task_sequence_id.prefix",
        "project_task_sequence_id.padding",
        "project_task_sequence_id.use_date_range",
        "project_task_sequence_id.active",
    )
    def _compute_task_sequence_setup(self):
        for department in self:
            sequence = department.project_task_sequence_id
            if not department.task_code_prefix or not sequence:
                department.task_sequence_status = "not_configured"
                department.task_sequence_preview = False
                continue
            if department._is_valid_task_sequence(sequence):
                department.task_sequence_status = "ready"
                department.task_sequence_preview = sequence.with_context(
                    ir_sequence_date=fields.Date.today(),
                    ir_sequence_date_range=fields.Date.today().replace(day=1),
                ).get_next_char(1)
            else:
                department.task_sequence_status = "invalid"
                department.task_sequence_preview = False

    def _get_expected_task_sequence_prefix(self):
        self.ensure_one()
        return "%s%%(range_month)s%%(range_y)s-" % (self.task_code_prefix or "")

    def _is_valid_task_sequence(self, sequence):
        self.ensure_one()
        if not sequence or not sequence.active:
            return False
        return (
            bool(self.task_code_prefix)
            and sequence.padding == 5
            and sequence.use_date_range
            and sequence.prefix == self._get_expected_task_sequence_prefix()
        )
```

- [ ] **Step 2: Add the Department actions that create and refresh the linked sequence**

```python
    def _prepare_task_sequence_values(self):
        self.ensure_one()
        if not self.task_code_prefix:
            raise ValidationError(_("Please set Task Code Prefix on Department first."))
        prefix = self.task_code_prefix.strip().upper()
        return {
            "name": "Task Sequence - %s" % self.name,
            "code": "department.task.%s.%s" % (self.id, prefix.lower()),
            "prefix": "%s%%(range_month)s%%(range_y)s-" % prefix,
            "padding": 5,
            "number_increment": 1,
            "number_next": 1,
            "use_date_range": True,
            "implementation": "standard",
            "company_id": self.company_id.id or False,
        }

    def action_create_task_sequence(self):
        for department in self:
            values = department._prepare_task_sequence_values()
            sequence = self.env["ir.sequence"].sudo().create(values)
            department.write({
                "task_code_prefix": department.task_code_prefix.strip().upper(),
                "project_task_sequence_id": sequence.id,
            })
        return True

    def action_refresh_task_sequence(self):
        for department in self:
            if not department.project_task_sequence_id:
                raise ValidationError(_("Please select Task Sequence on Department first."))
            values = department._prepare_task_sequence_values()
            department.project_task_sequence_id.sudo().write({
                "name": values["name"],
                "code": values["code"],
                "prefix": values["prefix"],
                "padding": values["padding"],
                "number_increment": values["number_increment"],
                "use_date_range": values["use_date_range"],
                "implementation": values["implementation"],
                "company_id": values["company_id"],
            })
            department.task_code_prefix = department.task_code_prefix.strip().upper()
        return True

    @api.constrains("task_code_prefix", "project_task_sequence_id")
    def _check_task_sequence_setup(self):
        for department in self.filtered("project_task_sequence_id"):
            if not department._is_valid_task_sequence(department.project_task_sequence_id):
                raise ValidationError(
                    _("Task Sequence must be active, use monthly date ranges, use padding 5, and match the Department prefix.")
                )
```

- [ ] **Step 3: Run the tests to verify the model behavior now passes**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -i autoinfo_project,dtr_project --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_project
```

Expected:

```text
The action and model tests pass, but the Department form view assertions still fail until the UI is updated
```

- [ ] **Step 4: Commit the Department model work**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\models\hr_department.py
git commit -m "feat: add department task sequence setup actions"
```

### Task 3: Expose Department Sequence Setup In The Form View

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml`
- Read: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`

- [ ] **Step 1: Add a dedicated setup group with fields, status, preview, and action buttons**

```xml
<!-- c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml -->
<?xml version="1.0" encoding="utf-8" ?>
<odoo>
    <record id="hr_department_form" model="ir.ui.view">
        <field name="name">hr.department.form</field>
        <field name="model">hr.department</field>
        <field name="inherit_id" ref="hr.view_department_form"/>
        <field name="arch" type="xml">
            <field name="company_id" position="after">
                <group string="Department Sequence Setup">
                    <group>
                        <field name="task_code_prefix"/>
                        <field name="project_task_sequence_id"/>
                    </group>
                    <group>
                        <field name="task_sequence_status" readonly="1"/>
                        <field name="task_sequence_preview" readonly="1"/>
                    </group>
                    <div class="oe_button_box" name="task_sequence_buttons">
                        <button name="action_create_task_sequence" type="object" string="Create Task Sequence" class="oe_highlight"/>
                        <button name="action_refresh_task_sequence" type="object" string="Refresh Task Sequence"/>
                    </div>
                </group>
                <field name="project_no_job_sequence_id"/>
                <field name="project_no_pm_sequence_id"/>
                <field name="project_no_service_sequence_id"/>
            </field>
        </field>
    </record>
</odoo>
```

- [ ] **Step 2: Run the tests to verify the form view exposes the new controls**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -i autoinfo_project,dtr_project --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_project
```

Expected:

```text
The Department setup view assertions pass, but task creation messages may still need cleanup in dtr_project
```

- [ ] **Step 3: Commit the Department view update**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml
git commit -m "feat: add department task sequence setup ui"
```

### Task 4: Make Project Task Consume Department Setup Cleanly

**Files:**
- Modify: `c:\odoo\addons_autoinfo\odoo15_mods\dtr_project\models\project_task.py`
- Read: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`

- [ ] **Step 1: Tighten the error messages so they point users back to Department setup**

```python
# c:\odoo\addons_autoinfo\odoo15_mods\dtr_project\models\project_task.py
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _get_creator_department(self, user):
        if not user or not user.employee_ids or not user.employee_ids[0].department_id:
            raise ValidationError("Please assign an Employee and Department to the task creator first.")
        return user.employee_ids[0].department_id

    def _prepare_creator_department_task_sequence(self, department):
        if "project_task_sequence_id" not in department._fields or not department.project_task_sequence_id:
            raise ValidationError("Please configure Task Sequence on Department first.")
        if "task_code_prefix" not in department._fields or not department.task_code_prefix:
            raise ValidationError("Please configure Task Code Prefix on Department first.")
        sequence = department.project_task_sequence_id.sudo()
        desired_prefix = "%s%%(range_month)s%%(range_y)s-" % department.task_code_prefix
        if sequence.prefix != desired_prefix or sequence.padding != 5 or not sequence.use_date_range:
            raise ValidationError("Department Task Sequence setup is invalid. Please refresh it from Department.")
        return sequence
```

- [ ] **Step 2: Keep task code generation by creator department and preserve the task title format**

```python
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code") and vals.get("code") != "New":
                continue
            vals["code"] = self._next_task_code_from_creator_department(self.env.user)
        return super().create(vals_list)

    def _compute_display_name(self):
        for rec in self:
            ref_parts = []
            if rec.code:
                ref_parts.append(rec.code)
            if rec.project_id:
                ref_parts.append(rec._get_project_job_no(rec.project_id))
            rec.display_name = "[%s] %s" % ("/".join(ref_parts), rec.name) if ref_parts else rec.name
```

- [ ] **Step 3: Run the full tests and the addon upgrade command**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -i autoinfo_project,dtr_project --test-enable --stop-after-init --log-level=test --test-tags /autoinfo_project
python c:\odoo\odoo-15.0\odoo-bin --addons-path="c:\odoo\odoo-15.0\addons,c:\odoo\addons_autoinfo\odoo15_mods,c:\odoo\addons_autoinfo\odoo15_mods_sales,c:\odoo\addons_autoinfo\odoo15_mods_purchase,c:\odoo\addons_autoinfo\custom15_autoinfo" -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --stop-after-init
```

Expected:

```text
All autoinfo_project tests pass, and both modules upgrade cleanly with no Python or XML errors
```

- [ ] **Step 4: Commit the task integration cleanup**

```powershell
git add c:\odoo\addons_autoinfo\odoo15_mods\dtr_project\models\project_task.py
git commit -m "feat: use department task setup for project task codes"
```

## Self-Review Checklist

- Spec coverage:
  - Department-only setup flow: covered by Tasks 2 and 3
  - Create or select sequence from Department: covered by Tasks 2 and 3
  - Task code by creator department: covered by Task 4
  - `[CODE/JOB NO] ชื่องาน`: covered by Task 4
  - Regression coverage: covered by Task 1
- Placeholder scan:
  - No `TODO`, `TBD`, or undefined implementation steps remain
- Type consistency:
  - `task_code_prefix`, `project_task_sequence_id`, `task_sequence_status`, `task_sequence_preview`, `action_create_task_sequence`, and `action_refresh_task_sequence` are used consistently across the plan
