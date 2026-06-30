# Installation Guide

## Prerequisites
- Odoo 15 with `hr_expense`, `mail`, and `analytic` available.
- Access to install custom addons.
- The custom addons root included in `addons_path`.

## Deployment Path
- Recommended module path: `/opt/odoo/custom15_autoinfo/autoinfo_hr_expense_duplicate_guard`
- Recommended `addons_path` entry: `/opt/odoo/custom15_autoinfo`

## Install Steps
1. Copy the module folder into the custom addons root.
2. Confirm `addons_path` includes the custom addons root.
3. Restart the Odoo service or application process.
4. Update the Apps list.
5. Install `AUTO INFO - HR Expense Duplicate Guard`.

## CLI Example
```bash
/opt/odoo/venv/bin/python /opt/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d hr_expense_duplicate_guard \
  -i autoinfo_hr_expense_duplicate_guard \
  --stop-after-init
```

## Upgrade Example
```bash
/opt/odoo/venv/bin/python /opt/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d hr_expense_duplicate_guard \
  -u autoinfo_hr_expense_duplicate_guard \
  --stop-after-init
```

## Post-Install Checks
- Open an expense form and confirm the `Duplicate Check` section is visible.
- Confirm approvers can see duplicate review columns on expense sheets.
- Confirm the security group `Expense Duplicate Override` exists under Human Resources.
- Create two similar expenses and verify duplicate state changes after submit or manual re-check logic.
- Confirm the override button appears only when the expense is `blocked` and the user belongs to the override group.

## Notes
- Duplicate checking runs during sheet submit and approval, so existing data quality matters during rollout.
- Refused expenses and expenses on cancelled sheets are intentionally ignored by the candidate search.
