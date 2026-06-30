# AUTO INFO - HR Expense Duplicate Guard (Odoo 15)

## Overview
- Prevents duplicate HR expense claims for mileage and monthly reimbursement flows.
- Extends `hr.expense` and `hr.expense.sheet` with duplicate review data, override metadata, and submit/approve guards.
- Stores duplicate evidence in `hr.expense.duplicate.hit` for reviewer visibility.
- Supports controlled override through a dedicated security group and reason capture.

## Current Functional Scope
- Adds `expense_guard_type` with `mileage`, `monthly`, and `other` options.
- Detects mileage duplicates when employee, route, normalized vehicle plate, and odometer ranges overlap.
- Detects monthly duplicates when employee, product, project, month, and year match.
- Adds a cross-type warning when a mileage claim resembles another trip-style expense for the same employee.
- Ignores refused expenses and expenses on cancelled sheets when building duplicate candidates.
- Re-checks duplicate state on both sheet submit and approval.
- Allows override only for users in `Expense Duplicate Override` with a required reason.

## Duplicate Outcomes
- `clear`: no duplicate evidence was found.
- `warning`: similar trip evidence exists, but the record is not blocked.
- `blocked`: one or more blocking duplicate hits exist and no override reason is stored.
- `overridden`: blocking evidence exists, but an authorized user saved an override reason.

## Rule Codes
- `mileage_overlap`: same route and vehicle with overlapping odometer ranges.
- `monthly_exact`: same employee, month, year, product, and analytic account.
- `cross_type_trip`: mileage claim resembles another trip-style expense and creates a warning only.

## UI Touchpoints
- Expense form: `Duplicate Check` section with guard inputs, review status, duplicate hits, and override action.
- Expense sheet form: `Duplicate Review` summary plus duplicate columns on expense lines.
- Override wizard: modal form that requires a non-blank reason.

## Security Summary
- `hr_expense.group_hr_expense_team_approver`: can read duplicate-hit records and use the override wizard.
- `Expense Duplicate Override`: inherits approver access and can save overrides.

## Installation Summary
1. Place the module in your custom addons path, for example `/opt/odoo/custom15_autoinfo/autoinfo_hr_expense_duplicate_guard`.
2. Make sure the custom addons root is present in `addons_path`.
3. Restart Odoo.
4. Update the Apps list.
5. Install `AUTO INFO - HR Expense Duplicate Guard`.

## Documentation
- `docs/installation_guide.md`
- `docs/user_guide.md`
- `docs/technical_guide.md`
- `docs/troubleshooting.md`
- `docs/timeline_and_changelog.md`

## Automated Tests
- `tests/test_expense_duplicate_guard.py`: validates duplicate-hit helpers, mileage/monthly detection, sheet blocking, override flow, and injected UI sections.

## Credits
Development Team: The Auto-Info Co., Ltd.

AI Coding Assistant: TRAE - used with human review for implementation support and documentation drafting.

## Changelog
- `15.0.1.0.0` - Initial delivery with duplicate-hit model, submit/approve guards, override wizard, security rules, views, tests, and module documentation.
