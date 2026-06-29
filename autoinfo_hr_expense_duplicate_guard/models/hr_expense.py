from odoo import _, api, fields, models


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

    def _get_duplicate_candidate_domain(self):
        self.ensure_one()
        return [
            ("id", "!=", self.id),
            ("employee_id", "=", self.employee_id.id),
            ("state", "!=", "refused"),
            "|",
            ("sheet_id", "=", False),
            ("sheet_id.state", "!=", "cancel"),
        ]

    def _run_duplicate_checks(self):
        for expense in self:
            expense._normalize_duplicate_values()
            expense._clear_duplicate_hits()
            expense._check_mileage_duplicates()
            expense._check_monthly_duplicates()
            expense._check_cross_type_duplicates()
            if any(hit.severity == "block" for hit in expense.duplicate_hit_ids):
                expense.duplicate_check_state = "blocked"
            elif expense.duplicate_hit_ids:
                expense.duplicate_check_state = "warning"
            elif expense.duplicate_override_reason:
                expense.duplicate_check_state = "overridden"
            else:
                expense.duplicate_check_state = "clear"
            expense.duplicate_summary = (
                ", ".join(expense.duplicate_hit_ids.mapped("reason_text")[:3]) or False
            )

    def _check_mileage_duplicates(self):
        self.ensure_one()
        if self.expense_guard_type != "mileage":
            return
        candidates = self.search(self._get_duplicate_candidate_domain())
        for candidate in candidates.filtered(lambda r: r.expense_guard_type == "mileage"):
            same_route = (
                self.trip_origin
                and self.trip_origin == candidate.trip_origin
                and self.trip_destination == candidate.trip_destination
                and self.vehicle_plate_normalized
                and self.vehicle_plate_normalized == candidate.vehicle_plate_normalized
            )
            overlap = (
                self.odometer_start <= candidate.odometer_end
                and self.odometer_end >= candidate.odometer_start
            )
            if same_route and overlap:
                self._create_duplicate_hit(
                    candidate,
                    "mileage_overlap",
                    "block",
                    _("ทะเบียนรถตรง และช่วงไมล์ซ้อน"),
                )

    def _check_monthly_duplicates(self):
        self.ensure_one()
        if self.expense_guard_type != "monthly":
            return
        candidates = self.search(self._get_duplicate_candidate_domain())
        for candidate in candidates.filtered(lambda r: r.expense_guard_type == "monthly"):
            same_bucket = (
                self.expense_month
                and self.expense_month == candidate.expense_month
                and self.expense_year == candidate.expense_year
                and self.product_id == candidate.product_id
                and self.analytic_account_id == candidate.analytic_account_id
            )
            if same_bucket:
                self._create_duplicate_hit(
                    candidate,
                    "monthly_exact",
                    "block",
                    _("เดือน ประเภท และโครงการตรงกัน"),
                )

    def _check_cross_type_duplicates(self):
        self.ensure_one()
        if self.expense_guard_type != "mileage":
            return
        candidates = self.search(self._get_duplicate_candidate_domain())
        for candidate in candidates.filtered(
            lambda r: r.expense_guard_type != self.expense_guard_type
        ):
            same_trip = (
                self.trip_origin
                and self.trip_origin == candidate.trip_origin
                and self.trip_destination == candidate.trip_destination
                and self.vehicle_plate_normalized
                and self.vehicle_plate_normalized == candidate.vehicle_plate_normalized
            )
            existing_hit = self.duplicate_hit_ids.filtered(
                lambda hit: hit.matched_expense_id == candidate
            )
            if same_trip and not existing_hit:
                self._create_duplicate_hit(
                    candidate,
                    "cross_type_trip",
                    "warning",
                    _("ข้อมูลการเดินทางคล้ายกับรายการเก่า"),
                )
