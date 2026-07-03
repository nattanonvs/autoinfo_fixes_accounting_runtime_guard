# Technical Guide

## Module Scope

The module extends `hr.expense` and `hr.expense.sheet` to support cash reimbursement tracking without creating petty cash documents.

## Main Components

- `models/hr_expense.py`: enforces analytic account requirements on expense lines
- `models/hr_expense_sheet.py`: adds cash tracking fields, tier validation guards, return cycle handling, and reimbursement audit logging
- `models/expense_approval_delegate.py`: resolves active delegates for the primary reviewer
- `models/expense_approval_role.py`: stores approval role to security group mapping
- `wizard/expense_return_reason_wizard.py`: sends expense sheets back to draft with return metadata
- `wizard/expense_cash_summary_xlsx_wizard.py`: prepares the sheet list for summary XLSX export
- `reports/expense_cash_detail_xlsx.py`: generates line-level XLSX output
- `reports/expense_cash_summary_xlsx.py`: generates sheet-level XLSX output

## Notifications

- Return notifications are posted from `hr.expense.sheet.write()` when the sheet enters the resubmission cycle.
- Reimbursement completion posts a chatter message after finance marks the payout as completed.

## Regression Coverage

- `tests/test_expense_cash_tracking_flow.py`
- `tests/test_expense_cash_tracking_security.py`
- `tests/test_expense_cash_tracking_xlsx.py`
