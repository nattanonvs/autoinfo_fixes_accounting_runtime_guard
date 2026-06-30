# Troubleshooting

## Module Does Not Appear In Apps
- Confirm the custom addons root is in `addons_path`.
- Restart Odoo after copying the module.
- Update the Apps list before searching for the module.

## Install Or Upgrade Fails
- Confirm dependencies `hr_expense`, `mail`, and `analytic` are available.
- Review errors from `security/`, `wizard/`, and `views/` first because they load during install.
- Run install or upgrade from CLI to capture the full traceback.

## Expense Is Not Blocked
- Confirm the expense belongs to the same employee as the candidate expense.
- Confirm the candidate expense is not `refused`.
- Confirm the candidate sheet is not cancelled.
- For mileage, confirm origin, destination, normalized plate, and odometer overlap all match.
- For monthly claims, confirm month, year, product, and analytic account all match.

## Warning Appears Instead Of Block
- Cross-type trip matches are designed as warnings only.
- Check `rule_code` in duplicate hits to confirm whether the hit is `cross_type_trip` or a blocking rule.

## Override Button Is Missing
- The expense must currently be in `blocked` state.
- The user must belong to `Expense Duplicate Override`.
- Re-run the relevant workflow step if duplicate data changed after the screen was opened.

## Override Fails
- Confirm the reason is not blank or whitespace only.
- Confirm the user belongs to `autoinfo_hr_expense_duplicate_guard.group_expense_duplicate_override`.

## Duplicate Summary Looks Incomplete
- `duplicate_summary` intentionally includes only the first few reason texts.
- Open the `Duplicate Hits` list on the expense to review all matching evidence.

## Approval Fails After Submit Already Passed
- The module re-checks duplicates during approval by design.
- Another similar expense may have been created after the sheet was submitted.
- Review the latest duplicate hits on each expense line before retrying.

## Vehicle Plate Matching Looks Wrong
- Plate comparison removes spaces and applies uppercase.
- Enter plates consistently if punctuation or special local formatting is used outside the current normalization logic.
