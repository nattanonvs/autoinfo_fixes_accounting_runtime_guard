from odoo import _, models
from odoo.exceptions import UserError


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def _run_duplicate_checks_for_expense_lines(self):
        self.mapped("expense_line_ids")._run_duplicate_checks()

    def _raise_duplicate_block_if_needed(self):
        blocked_expenses = self.mapped("expense_line_ids").filtered(
            lambda expense: expense.duplicate_check_state == "blocked"
        )
        if blocked_expenses:
            blocked_names = ", ".join(blocked_expenses.mapped("name"))
            raise UserError(_("Duplicate expense detected: %s") % blocked_names)

    def action_submit_sheet(self):
        self._run_duplicate_checks_for_expense_lines()
        self._raise_duplicate_block_if_needed()
        return super().action_submit_sheet()

    def approve_expense_sheets(self):
        self._run_duplicate_checks_for_expense_lines()
        self._raise_duplicate_block_if_needed()
        return super().approve_expense_sheets()
