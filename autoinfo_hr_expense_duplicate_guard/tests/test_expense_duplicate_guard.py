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
