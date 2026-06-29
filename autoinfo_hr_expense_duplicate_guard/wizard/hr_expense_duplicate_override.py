from odoo import _, fields, models
from odoo.exceptions import UserError


class HrExpenseDuplicateOverride(models.TransientModel):
    _name = "hr.expense.duplicate.override"
    _description = "HR Expense Duplicate Override"

    expense_id = fields.Many2one("hr.expense", required=True)
    reason = fields.Text(required=True)

    def action_confirm(self):
        self.ensure_one()
        if not (self.reason or "").strip():
            raise UserError(_("Override reason is required."))
        self.expense_id.action_apply_duplicate_override(self.reason)
        return {"type": "ir.actions.act_window_close"}
