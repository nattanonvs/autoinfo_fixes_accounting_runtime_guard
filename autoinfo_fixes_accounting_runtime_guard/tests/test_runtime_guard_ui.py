from lxml import etree

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("runtime_guard_ui", "-at_install", "post_install")
class TestRuntimeGuardUi(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.system_user = cls.env.ref("base.user_admin")
        cls.normal_user = cls.env["res.users"].with_context(
            no_reset_password=True
        ).create(
            {
                "name": "Runtime Guard Normal User",
                "login": "runtime_guard_normal_user",
                "email": "runtime_guard_normal_user@example.com",
                "password": "test-password",
                "groups_id": [(6, 0, [cls.env.ref("base.group_user").id])],
            }
        )
        cls.guard_run = cls.env["autoinfo.runtime.guard.run"].create(
            {
                "name": "UI Test Run",
                "run_scope": "manual",
            }
        )
        cls.check = cls.env["autoinfo.runtime.guard.check"].create(
            {
                "run_id": cls.guard_run.id,
                "name": "Dependency Chain Risk",
                "check_code": "dependency_chain_dtr_billing",
                "category": "dependency_chain",
                "severity": "error",
                "state": "error",
                "summary": "Field actual_due_date may load without dtr_billing",
                "details": "Module dtr_customer_invoices_with_sales appears to need dtr_billing",
                "recommended_action": "Add the dependency and rerun upgrade",
                "fix_command": "sed -i ...",
                "verify_command": "grep -n dtr_billing ...",
                "is_safe_fix": False,
                "needs_review": True,
            }
        )

    def test_fix_help_action_opens_transient_wizard(self):
        action = self.check.action_open_fix_help()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "autoinfo.runtime.guard.fix.help")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_check_id"], self.check.id)

    def test_mark_reviewed_stamps_user_and_time(self):
        self.check.with_user(self.system_user).action_mark_reviewed()

        self.assertEqual(self.check.state, "review")
        self.assertEqual(self.check.reviewed_by, self.system_user)
        self.assertTrue(self.check.reviewed_on)

    def test_runtime_guard_menu_is_limited_to_system_group(self):
        menu = self.env.ref(
            "autoinfo_fixes_accounting_runtime_guard.menu_runtime_guard_root"
        )
        self.assertEqual(menu.groups_id.ids, [self.env.ref("base.group_system").id])

    def test_runtime_guard_forms_expose_expected_buttons(self):
        run_view = self.env.ref(
            "autoinfo_fixes_accounting_runtime_guard.view_runtime_guard_run_form"
        )
        run_root = etree.fromstring(run_view.get_combined_arch().encode())

        view = self.env.ref(
            "autoinfo_fixes_accounting_runtime_guard.view_runtime_guard_check_form"
        )
        root = etree.fromstring(view.get_combined_arch().encode())

        run_buttons = run_root.xpath(".//button[@name='action_run_checks']")
        fix_buttons = root.xpath(".//button[@name='action_open_fix_help']")
        review_buttons = root.xpath(".//button[@name='action_mark_reviewed']")

        self.assertEqual(len(run_buttons), 1)
        self.assertEqual(len(fix_buttons), 1)
        self.assertEqual(len(review_buttons), 1)
