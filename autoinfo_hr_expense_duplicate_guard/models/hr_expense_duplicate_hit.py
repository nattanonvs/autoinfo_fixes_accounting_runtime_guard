from odoo import fields, models


class HrExpenseDuplicateHit(models.Model):
    _name = "hr.expense.duplicate.hit"
    _description = "HR Expense Duplicate Hit"
    _order = "severity desc, id desc"

    expense_id = fields.Many2one("hr.expense", required=True, ondelete="cascade")
    matched_expense_id = fields.Many2one(
        "hr.expense",
        required=True,
        ondelete="cascade",
    )
    rule_code = fields.Char(required=True)
    severity = fields.Selection(
        [
            ("warning", "Warning"),
            ("block", "Block"),
        ],
        required=True,
    )
    reason_text = fields.Char(required=True)
    matched_state = fields.Char()
