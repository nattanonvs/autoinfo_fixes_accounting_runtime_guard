from odoo.tests.common import TransactionCase


class TestExpenseDuplicateGuard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env.user.employee_id or cls.env["hr.employee"].create(
            {
                "name": "Expense Guard Employee",
                "company_id": cls.env.company.id,
            }
        )
        cls.expense_product = cls.env["product.product"].create(
            {
                "name": "Expense Guard Product",
                "type": "service",
                "can_be_expensed": True,
            }
        )
        cls.monthly_product = cls.env["product.product"].create(
            {
                "name": "Monthly Expense Product",
                "type": "service",
                "can_be_expensed": True,
            }
        )
        cls.other_product = cls.env["product.product"].create(
            {
                "name": "Other Expense Product",
                "type": "service",
                "can_be_expensed": True,
            }
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Expense Guard Project",
                "company_id": cls.env.company.id,
            }
        )

    def _create_mileage_expense(self, name, **overrides):
        values = {
            "name": name,
            "employee_id": self.employee.id,
            "product_id": self.expense_product.id,
            "date": "2026-06-26",
            "unit_amount": 100.0,
            "quantity": 1.0,
            "expense_guard_type": "mileage",
            "trip_date_from": "2026-06-26",
            "trip_date_to": "2026-06-26",
            "trip_origin": "Office",
            "trip_destination": "Site A",
            "vehicle_plate": "1กข 1234",
            "odometer_start": 100.0,
            "odometer_end": 150.0,
        }
        values.update(overrides)
        return self.env["hr.expense"].create(values)

    def _create_monthly_expense(self, name, **overrides):
        values = {
            "name": name,
            "employee_id": self.employee.id,
            "product_id": self.monthly_product.id,
            "date": "2026-06-26",
            "unit_amount": 500.0,
            "quantity": 1.0,
            "expense_guard_type": "monthly",
            "expense_month": 6,
            "expense_year": 2026,
            "analytic_account_id": self.analytic_account.id,
        }
        values.update(overrides)
        return self.env["hr.expense"].create(values)

    def _create_other_trip_expense(self, name, **overrides):
        values = {
            "name": name,
            "employee_id": self.employee.id,
            "product_id": self.other_product.id,
            "date": "2026-06-26",
            "unit_amount": 100.0,
            "quantity": 1.0,
            "expense_guard_type": "other",
            "trip_date_from": "2026-06-26",
            "trip_date_to": "2026-06-26",
            "trip_origin": "Office",
            "trip_destination": "Site A",
            "vehicle_plate": "1กข 1234",
            "odometer_start": 100.0,
            "odometer_end": 150.0,
        }
        values.update(overrides)
        return self.env["hr.expense"].create(values)

    def test_expense_duplicate_defaults(self):
        expense = self._create_mileage_expense("Mileage A")

        self.assertEqual(expense.duplicate_check_state, "clear")
        self.assertEqual(expense.vehicle_plate_normalized, "1กข1234")

    def test_normalize_duplicate_values_sets_month_and_year_from_date(self):
        expense = self._create_mileage_expense(
            "Mileage B",
            expense_month=False,
            expense_year=False,
        )

        expense._normalize_duplicate_values()

        self.assertEqual(expense.expense_month, 6)
        self.assertEqual(expense.expense_year, 2026)

    def test_duplicate_hit_helpers_create_and_clear_hits(self):
        expense = self._create_mileage_expense("Mileage C")
        matched_expense = self._create_mileage_expense(
            "Mileage D",
            vehicle_plate="2กข 4567",
            odometer_start=200.0,
            odometer_end=250.0,
        )

        hit = expense._create_duplicate_hit(
            matched_expense,
            "mileage_overlap",
            "block",
            "Mileage overlaps an existing expense.",
        )

        self.assertEqual(expense.duplicate_hit_ids, hit)
        self.assertEqual(hit.matched_state, matched_expense.state)

        expense._clear_duplicate_hits()

        self.assertFalse(expense.duplicate_hit_ids)

    def test_mileage_overlap_creates_block_hit(self):
        self._create_mileage_expense("Trip 1", odometer_start=100.0, odometer_end=150.0)
        duplicate = self._create_mileage_expense(
            "Trip 2",
            odometer_start=120.0,
            odometer_end=160.0,
        )

        duplicate._run_duplicate_checks()

        self.assertEqual(duplicate.duplicate_check_state, "blocked")
        self.assertEqual(duplicate.duplicate_hit_ids[:1].rule_code, "mileage_overlap")

    def test_monthly_same_employee_type_month_project_blocks(self):
        self._create_monthly_expense("Fuel Jun A")
        duplicate = self._create_monthly_expense("Fuel Jun B")

        duplicate._run_duplicate_checks()

        self.assertEqual(duplicate.duplicate_check_state, "blocked")
        self.assertEqual(duplicate.duplicate_hit_ids[:1].rule_code, "monthly_exact")

    def test_cross_type_trip_creates_warning(self):
        self._create_other_trip_expense("Trip A")
        duplicate = self._create_mileage_expense(
            "Trip B",
            odometer_start=151.0,
            odometer_end=180.0,
        )

        duplicate._run_duplicate_checks()

        self.assertEqual(duplicate.duplicate_check_state, "warning")
        self.assertEqual(duplicate.duplicate_hit_ids[:1].rule_code, "cross_type_trip")
