# Troubleshooting

## Cannot Submit Expense Sheet

- Check that every expense line has an analytic account.
- Confirm the sheet is not blocked by tier validation that is still pending.

## Finance Cannot Mark Cash Reimbursed

- Verify the user belongs to `group_expense_cash_reimbursement_manager`.
- Confirm the action is executed from the expense sheet workflow and not from a user without finance permission.

## Return Notification Not Visible

- Open the chatter on the expense sheet and verify that the return action was confirmed from the wizard.
- Check that the sheet has `returned_for_resubmission` enabled together with a return tier and reason.

## XLSX Export Problems

- Ensure `report_xlsx` is installed and loaded in the environment.
- Verify that the expense sheet or wizard date range returns records before exporting.
