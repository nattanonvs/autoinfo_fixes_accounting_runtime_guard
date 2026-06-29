from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestTask2Skeleton(TransactionCase):
    def test_duplicate_hit_model_is_registered(self):
        self.assertIn("hr.expense.duplicate.hit", self.env)

    def test_override_wizard_requires_non_blank_reason(self):
        wizard = self.env["hr.expense.duplicate.override"].new(
            {
                "reason": "   ",
            }
        )

        with self.assertRaises(UserError):
            wizard.action_confirm()
