# User Guide

## Purpose
This module helps HR expense reviewers detect duplicate reimbursement claims before approval, while still allowing controlled exceptions with an auditable reason.

## Access Rights
- Expense submitters can fill in duplicate-check fields on expenses.
- `hr_expense.group_hr_expense_team_approver` can review duplicate hits and use the override wizard.
- `Expense Duplicate Override` can save an override reason and continue the blocked flow.

## Expense Types
- `Mileage`: used for trip claims based on route, vehicle, and odometer data.
- `Monthly`: used for recurring monthly reimbursement checks.
- `Other`: does not trigger the monthly block logic and is used as the cross-type comparison source for trip warnings.

## Enter a Mileage Expense
1. Open or create an expense.
2. Set `Expense Guard Type` to `Mileage`.
3. Fill `Trip Date From`, `Trip Date To`, `Trip Origin`, `Trip Destination`, `Vehicle Plate`, `Odometer Start`, and `Odometer End`.
4. Save the expense.
5. Review `Duplicate Check State` and `Duplicate Summary`.

## Enter a Monthly Expense
1. Open or create an expense.
2. Set `Expense Guard Type` to `Monthly`.
3. Fill `Expense Month`, `Expense Year`, product, employee, and project (`Analytic Account`).
4. Save the expense.
5. Review the duplicate status before submitting the sheet.

## Review Duplicate Evidence
- `Duplicate Check State` shows whether the record is clear, warning, blocked, or overridden.
- `Duplicate Summary` shows a short summary of the first matching reasons.
- `Duplicate Hits` lists severity, rule code, reason text, the matched expense, and its state.
- Expense sheets show duplicate status columns so approvers can review multiple lines together.

## Submit and Approve Behavior
- Sheet submit runs duplicate checks on all expense lines.
- Approval runs duplicate checks again to catch duplicates created after submission.
- If any line remains `blocked`, the sheet action raises an error and stops.
- Warning-only hits do not block submit or approval.

## Override a Blocked Expense
1. Open the blocked expense.
2. Confirm the button `Override Duplicate Block` is visible.
3. Click the button.
4. Enter a non-blank reason.
5. Confirm the wizard.
6. Review the saved override metadata and continue the normal sheet workflow.

## Important Notes
- Override does not remove duplicate hits; it records an approved exception.
- The module ignores refused expenses and expenses on cancelled sheets during matching.
- Vehicle plate normalization removes spaces and applies uppercase before comparison.
