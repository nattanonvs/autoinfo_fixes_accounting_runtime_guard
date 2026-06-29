from odoo import api, fields, models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    expense_guard_type = fields.Selection(
        [
            ("mileage", "Mileage"),
            ("monthly", "Monthly"),
            ("other", "Other"),
        ],
        default="other",
        tracking=True,
    )
    trip_date_from = fields.Date()
    trip_date_to = fields.Date()
    trip_origin = fields.Char()
    trip_destination = fields.Char()
    vehicle_plate = fields.Char()
    vehicle_plate_normalized = fields.Char(
        compute="_compute_vehicle_plate_normalized",
        store=True,
    )
    odometer_start = fields.Float()
    odometer_end = fields.Float()
    expense_month = fields.Integer()
    expense_year = fields.Integer()
    duplicate_check_state = fields.Selection(
        [
            ("clear", "Clear"),
            ("warning", "Warning"),
            ("blocked", "Blocked"),
            ("overridden", "Overridden"),
        ],
        default="clear",
        tracking=True,
    )
    duplicate_summary = fields.Char()
    duplicate_hit_ids = fields.One2many(
        "hr.expense.duplicate.hit",
        "expense_id",
    )
    duplicate_override_reason = fields.Text(readonly=True)
    duplicate_override_by = fields.Many2one("res.users", readonly=True)
    duplicate_override_date = fields.Datetime(readonly=True)

    @api.depends("vehicle_plate")
    def _compute_vehicle_plate_normalized(self):
        for expense in self:
            expense.vehicle_plate_normalized = (
                (expense.vehicle_plate or "").replace(" ", "").upper()
            )

    def _normalize_duplicate_values(self):
        for expense in self:
            if expense.date and not expense.expense_month:
                expense.expense_month = expense.date.month
            if expense.date and not expense.expense_year:
                expense.expense_year = expense.date.year

    def _clear_duplicate_hits(self):
        self.mapped("duplicate_hit_ids").unlink()

    def _create_duplicate_hit(self, matched_expense, rule_code, severity, reason_text):
        self.ensure_one()
        return self.env["hr.expense.duplicate.hit"].create(
            {
                "expense_id": self.id,
                "matched_expense_id": matched_expense.id,
                "rule_code": rule_code,
                "severity": severity,
                "reason_text": reason_text,
                "matched_state": matched_expense.state,
            }
        )
