from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrExpense(models.Model):
    _inherit = "hr.expense"

    analytic_account_required = fields.Boolean(
        compute="_compute_analytic_account_required",
        readonly=True,
    )

    @api.depends("company_id", "account_id")
    def _compute_analytic_account_required(self):
        for expense in self:
            expense.analytic_account_required = True

    def _check_cash_tracking_analytic_account(self):
        for expense in self:
            if not expense.analytic_account_id:
                raise UserError(
                    _(
                        "Every expense line must have an Analytic Account before this report can be submitted."
                    )
                )

