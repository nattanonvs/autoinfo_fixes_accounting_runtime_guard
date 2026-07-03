# Installation Guide

## Prerequisites

- Odoo 15 environment with access to the custom addons path
- Dependencies installed: `hr_expense`, `mail`, `analytic`, `report_xlsx`, `base_tier_validation`, `dtr_expense_tier_validation`
- Test database available for upgrade and regression validation

## Install Or Upgrade

```powershell
& 'c:\odoo\odoo-15.0\.venv\Scripts\python.exe' 'c:\odoo\odoo-15.0\odoo-bin' `
  -c 'c:\odoo\odoo-15.0\odoo.conf' `
  -d 'expense_cash_tracking_plan' `
  --stop-after-init `
  -u 'autoinfo_hr_expense_cash_tracking'
```

## Post-Install Checklist

1. Assign security groups for accounting reviewers, executive viewers, and reimbursement managers.
2. Confirm tier definitions exist for the expense approval flow.
3. Verify employees and expense managers are configured correctly.
4. Open an expense sheet form and confirm the cash tracking section is visible.
5. Validate both detail and summary XLSX export actions.
