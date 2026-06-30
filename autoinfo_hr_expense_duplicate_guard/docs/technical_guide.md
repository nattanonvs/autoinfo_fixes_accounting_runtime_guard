# Technical Guide

## Module Summary
- Module name: `autoinfo_hr_expense_duplicate_guard`
- Odoo version target: 15.0
- Main business purpose: prevent duplicate HR expense claims while preserving a controlled exception workflow.

## Main Components
- `models/hr_expense.py`
  - extends `hr.expense` with duplicate-check fields and detection logic.
  - computes normalized vehicle plate values.
  - stores duplicate summary and override metadata.
- `models/hr_expense_duplicate_hit.py`
  - stores reviewable duplicate-hit evidence per expense.
- `models/hr_expense_sheet.py`
  - runs duplicate checks before submit and approval.
  - blocks sheet actions when any expense line remains blocked.
- `wizard/hr_expense_duplicate_override.py`
  - requires a non-blank reason and delegates override persistence to `hr.expense`.
- `views/hr_expense_views.xml`
  - injects the duplicate review section and override button into the expense form.
- `views/hr_expense_sheet_views.xml`
  - surfaces duplicate review information on the expense sheet.

## Core Data Fields
- `expense_guard_type`: classifies duplicate logic into `mileage`, `monthly`, or `other`.
- `vehicle_plate_normalized`: stored computed plate value with spaces removed and uppercase applied.
- `duplicate_check_state`: final review outcome.
- `duplicate_summary`: short text summary built from the first matching reasons.
- `duplicate_hit_ids`: one2many to `hr.expense.duplicate.hit`.
- `duplicate_override_reason`, `duplicate_override_by`, `duplicate_override_date`: audit trail for exceptions.

## Candidate Selection Logic
The duplicate candidate domain is restricted to:
- same employee,
- different expense record,
- expense state not equal to `refused`, and
- either no sheet or a sheet whose state is not `cancel`.

## Detection Rules
### Mileage Block
A block hit is created when all of these are true:
- the current expense type is `mileage`,
- origin matches,
- destination matches,
- normalized vehicle plate matches, and
- odometer ranges overlap.

### Monthly Block
A block hit is created when all of these are true:
- the current expense type is `monthly`,
- month matches,
- year matches,
- product matches, and
- analytic account matches.

### Cross-Type Warning
A warning hit is created when:
- the current expense type is `mileage`,
- a candidate has a different `expense_guard_type`, and
- origin, destination, and normalized vehicle plate match.

## State Resolution
After all rule checks finish:
- `overridden` wins when block hits exist and an override reason is already stored.
- `blocked` is used when at least one block hit exists without override.
- `warning` is used when only warning hits exist.
- `clear` is used when no hits exist.

## Workflow Enforcement
1. Expense sheet submit calls `_run_duplicate_checks_for_expense_lines()`.
2. The sheet collects blocked lines in `_raise_duplicate_block_if_needed()`.
3. If blocked lines exist, a `UserError` stops the workflow.
4. The same enforcement runs again in `approve_expense_sheets()`.

## Security Model
- `group_expense_duplicate_override` is defined in `security/expense_duplicate_security.xml`.
- The group implies `hr_expense.group_hr_expense_team_approver`.
- Access rights in `security/ir.model.access.csv` allow approvers to read duplicate hits and use the wizard.
- Override-group members have full access to duplicate-hit records so overrides can persist new review evidence.

## Automated Tests
- `tests/test_expense_duplicate_guard.py`
  - validates field defaults and normalization.
  - validates duplicate-hit helper creation and cleanup.
  - validates mileage, monthly, and cross-type detection paths.
  - validates ignored candidates such as refused expenses and cancelled sheets.
  - validates submit blocking, approval re-checks, and override behavior.
  - validates injected UI sections on expense and sheet forms.

## Known Scope Limits
- Duplicate checking is scoped to the same employee only.
- Cross-type comparison currently runs only when the active expense is `mileage`.
- The module does not add a scheduled re-scan job; checks happen during explicit workflow actions and direct method calls.
