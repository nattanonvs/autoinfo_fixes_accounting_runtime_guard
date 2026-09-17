from unittest.mock import patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("runtime_guard_service", "-at_install", "post_install")
class TestRuntimeGuardService(TransactionCase):
    def test_run_checks_creates_one_record_per_result(self):
        run = self.env["autoinfo.runtime.guard.run"].create(
            {
                "name": "Manual Runtime Guard Run",
                "run_scope": "manual",
            }
        )

        fake_results = [
            {
                "name": "Runtime Path",
                "check_code": "runtime_path",
                "category": "runtime",
                "severity": "ok",
                "state": "ok",
                "summary": "Runtime path matches expected Linux command",
                "details": "python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf",
                "recommended_action": "Keep current command",
                "fix_command": False,
                "verify_command": "python3 /var/odoo/odoo15/odoo-bin --version",
                "is_safe_fix": False,
                "needs_review": False,
            },
            {
                "name": "PyPDF2 Package",
                "check_code": "python_package_pypdf2",
                "category": "python_package",
                "severity": "error",
                "state": "error",
                "summary": "PyPDF2 missing in runtime interpreter",
                "details": "Import failed for PyPDF2",
                "recommended_action": "Install package into the same Python used by Odoo",
                "fix_command": "python3 -m pip install PyPDF2",
                "verify_command": "python3 -c \"import PyPDF2\"",
                "is_safe_fix": False,
                "needs_review": True,
            },
        ]

        with patch.object(
            type(run),
            "_build_v1_results",
            return_value=fake_results,
        ):
            run.action_run_checks()

        self.assertEqual(run.result_count, 2)
        self.assertEqual(run.warning_count, 0)
        self.assertEqual(run.error_count, 1)
        self.assertEqual(len(run.check_ids), 2)
        self.assertEqual(
            run.check_ids.mapped("check_code"),
            ["runtime_path", "python_package_pypdf2"],
        )

    def test_dependency_chain_result_marks_dtr_billing_risk(self):
        run = self.env["autoinfo.runtime.guard.run"].create(
            {
                "name": "Dependency Risk Run",
                "run_scope": "manual",
            }
        )

        with patch.object(
            type(run),
            "_find_dependency_chain_risks",
            return_value=[
                {
                    "module_name": "dtr_customer_invoices_with_sales",
                    "field_name": "actual_due_date",
                    "missing_dependency": "dtr_billing",
                }
            ],
        ):
            results = run._build_dependency_chain_results()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["severity"], "error")
        self.assertIn("dtr_billing", results[0]["details"])
        self.assertIn("actual_due_date", results[0]["summary"])

    def test_schema_risk_result_marks_missing_actual_due_date(self):
        run = self.env["autoinfo.runtime.guard.run"].create(
            {
                "name": "Schema Risk Run",
                "run_scope": "manual",
            }
        )

        with patch.object(
            type(run),
            "_detect_schema_risks",
            return_value=[
                {
                    "model": "account.move",
                    "field": "actual_due_date",
                    "root_cause": "module_not_upgraded",
                }
            ],
        ):
            results = run._build_schema_risk_results()

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["check_code"],
            "schema_risk_account_move_actual_due_date",
        )
        self.assertEqual(results[0]["severity"], "error")
        self.assertIn("module_not_upgraded", results[0]["details"])

    def test_module_state_result_summarizes_to_upgrade_backlog(self):
        run = self.env["autoinfo.runtime.guard.run"].create(
            {
                "name": "Module State Run",
                "run_scope": "manual",
            }
        )

        with patch.object(
            type(run),
            "_get_modules_to_upgrade",
            return_value=["dtr_billing", "dtr_payment_invoice"],
        ):
            results = run._build_module_state_results()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["severity"], "warning")
        self.assertIn("dtr_billing", results[0]["details"])
        self.assertIn("string_agg", results[0]["fix_command"])
