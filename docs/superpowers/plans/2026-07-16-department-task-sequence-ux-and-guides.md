# Department Task Sequence UX And Guides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve Department sequence setup UX by showing only valid actions per state, and provide user/admin guides for repeated BA/TA/IA/FA/DES operations.

**Architecture:** Keep backend validation intact and add view-level button visibility conditions driven by `project_task_sequence_id`. Add one small UI regression test to lock the visibility behavior. Add two documentation files: one user workflow guide and one admin/test runbook using the verified `odoo.conf` command path.

**Tech Stack:** Odoo 15 CE, XML inherited views, Python transactional tests (`TransactionCase` + `lxml`), Markdown docs

---

## File Map

- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml`
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\user_guide.md`
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\admin_test_guide.md`

## Test Command Baseline

Run this after each code task:

```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --test-enable --test-tags /autoinfo_project --stop-after-init --log-level=test
```

Expected success signal:

```text
... 0 failed, 0 error(s) ...
```

### Task 1: Lock UX Behavior With A Failing Test

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`

- [ ] **Step 1: Add a failing test for Create/Refresh visibility by setup state**

```python
    def test_department_form_shows_only_valid_action_by_sequence_state(self):
        result_before = self.department_model.fields_view_get(view_type="form")
        doc_before = etree.fromstring(result_before["arch"].encode())

        create_buttons_before = doc_before.xpath(
            "//button[@name='action_create_task_sequence']"
        )
        refresh_buttons_before = doc_before.xpath(
            "//button[@name='action_refresh_task_sequence']"
        )

        self.assertTrue(create_buttons_before)
        self.assertTrue(refresh_buttons_before)
        self.assertIn("project_task_sequence_id", create_buttons_before[0].get("attrs", ""))
        self.assertIn("project_task_sequence_id", refresh_buttons_before[0].get("attrs", ""))

        self.department.action_create_task_sequence()
        result_after = self.department_model.fields_view_get(view_type="form")
        doc_after = etree.fromstring(result_after["arch"].encode())
        create_buttons_after = doc_after.xpath("//button[@name='action_create_task_sequence']")
        refresh_buttons_after = doc_after.xpath("//button[@name='action_refresh_task_sequence']")

        self.assertTrue(create_buttons_after)
        self.assertTrue(refresh_buttons_after)
```

- [ ] **Step 2: Run tests and confirm this new UX test fails for missing attrs logic**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --test-enable --test-tags /autoinfo_project --stop-after-init --log-level=test
```

Expected:

```text
FAIL: button attrs visibility conditions are missing or incorrect in hr_department_view.xml
```

- [ ] **Step 3: Commit the failing test**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py
git commit -m "test: add department sequence action visibility regression"
```

### Task 2: Implement Department Button Visibility

**Files:**
- Modify: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml`
- Read: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\tests\test_department_task_sequence_setup.py`

- [ ] **Step 1: Add attrs visibility rules on Create/Refresh buttons**

```xml
<button
    name="action_create_task_sequence"
    type="object"
    string="Create Task Sequence"
    class="oe_highlight"
    attrs="{'invisible': [('project_task_sequence_id', '!=', False)]}"
/>
<button
    name="action_refresh_task_sequence"
    type="object"
    string="Refresh Task Sequence"
    attrs="{'invisible': [('project_task_sequence_id', '=', False)]}"
/>
```

- [ ] **Step 2: Run tests and verify all UX + setup tests pass**

Run:

```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --test-enable --test-tags /autoinfo_project --stop-after-init --log-level=test
```

Expected:

```text
All autoinfo_project sequence setup tests pass including visibility checks
```

- [ ] **Step 3: Commit the view UX change**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\views\hr_department_view.xml
git commit -m "feat: show department sequence actions by setup state"
```

### Task 3: Write User Guide For BA/TA/IA/FA/DES Flow

**Files:**
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\user_guide.md`

- [ ] **Step 1: Create a concise Thai user guide with real workflow steps**

```markdown
# คู่มือผู้ใช้งาน Task Sequence ตามแผนก

## ใช้เมื่อไร
- ใช้เมื่อต้องตั้งค่าเลขงานของแผนก เช่น BA, TA, IA, FA, DES

## ขั้นตอนตั้งค่าครั้งแรก
1. ไปที่เมนู Department
2. เปิดแผนกที่ต้องการ
3. กรอก `Task Code Prefix` เช่น `BA`
4. กด `Create Task Sequence`
5. ตรวจสอบ `Task Sequence Status` ต้องเป็น `Ready`
6. ดู `Task Sequence Preview` ตัวอย่างเช่น `BA0126-00001`

## ขั้นตอนปรับปรุงการตั้งค่า
1. เปิด Department เดิม
2. แก้ `Task Code Prefix` หรือเลือก `Task Sequence` ที่ต้องการ
3. กด `Refresh Task Sequence`
4. ตรวจสอบว่า `Status` กลับมาเป็น `Ready`

## ตัวอย่างเลขงาน
- BA: `BA0126-00001`
- TA: `TA0126-00001`
- IA: `IA0126-00001`
- FA: `FA0126-00001`
- DES: `DES0126-00001`

## ถ้าเจอปัญหา
- ข้อความ `Please complete Department Sequence Setup first.`:
  ตั้งค่า Prefix และ Task Sequence ที่หน้า Department ให้ครบ
- ข้อความ `Department Sequence Setup is invalid.`:
  กด `Refresh Task Sequence` ที่หน้า Department
```

- [ ] **Step 2: Validate markdown file exists and is readable**

Run:

```powershell
python -c "from pathlib import Path; p=Path(r'c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\user_guide.md'); print(p.exists(), p.stat().st_size > 0)"
```

Expected:

```text
True True
```

- [ ] **Step 3: Commit user guide**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\user_guide.md
git commit -m "docs: add department task sequence user guide"
```

### Task 4: Write Admin/Test Runbook

**Files:**
- Create: `c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\admin_test_guide.md`

- [ ] **Step 1: Create admin/test guide with copy-paste commands**

```markdown
# คู่มือ Admin/Test สำหรับ Department Task Sequence

## Config ที่ใช้งาน
- ใช้ไฟล์: `c:\odoo\odoo-15.0\odoo.conf`
- path สำคัญที่ต้องมีใน addons_path:
  - `c:\odoo\addons_autoinfo\odoo15_apps_oca_purchase_workflow`
  - ต้องไม่มี `c:\odoo\addons_oca\apps-store`

## คำสั่ง Upgrade มาตรฐาน
```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --stop-after-init --log-level=info
```

## คำสั่ง Test มาตรฐาน
```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --test-enable --test-tags /autoinfo_project --stop-after-init --log-level=test
```

## ตรวจสอบเบื้องต้นเมื่อเลข Task ไม่ออก
1. ตรวจ user ผู้สร้างมี employee + department
2. ตรวจ Department มี `Task Code Prefix`
3. ตรวจ Department มี `Task Sequence`
4. ตรวจ `Task Sequence Status = Ready`
5. กด `Refresh Task Sequence` แล้วลองใหม่

## Warnings ที่พบได้ (ไม่ใช่ blocker)
- `selection overrides existing selection`
- `unable to set NOT NULL on project_task.task_category_id/project_site_id`
```

- [ ] **Step 2: Validate markdown file exists and is readable**

Run:

```powershell
python -c "from pathlib import Path; p=Path(r'c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\admin_test_guide.md'); print(p.exists(), p.stat().st_size > 0)"
```

Expected:

```text
True True
```

- [ ] **Step 3: Commit admin/test guide**

```powershell
git add c:\odoo\addons_autoinfo\custom15_autoinfo\autoinfo_project\docs\admin_test_guide.md
git commit -m "docs: add department task sequence admin test runbook"
```

## Self-Review Checklist

- Spec coverage:
  - Hide `Create` when sequence exists: covered by Tasks 1-2
  - Show `Refresh` only when sequence exists: covered by Tasks 1-2
  - User guide for BA/TA/IA/FA/DES: covered by Task 3
  - Admin/test command reuse: covered by Task 4
- Placeholder scan:
  - No `TODO` or unresolved implementation placeholders
- Type consistency:
  - Uses existing fields/actions consistently: `project_task_sequence_id`, `action_create_task_sequence`, `action_refresh_task_sequence`
