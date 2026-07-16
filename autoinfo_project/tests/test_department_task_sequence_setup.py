from lxml import etree

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestDepartmentTaskSequenceSetup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department_model = cls.env["hr.department"]
        cls.sequence_model = cls.env["ir.sequence"]
        cls.user_model = cls.env["res.users"]
        cls.employee_model = cls.env["hr.employee"]
        cls.task_model = cls.env["project.task"]
        cls.project_model = cls.env["project.project"]
        cls.category_model = cls.env["project.task.category"]
        cls.site_model = cls.env["project.site"]
        cls.db_model = cls.env["project.site.database"]

        cls.department = cls.department_model.create(
            {
                "name": "Business Analyst",
                "task_code_prefix": "BA",
            }
        )
        cls.user = cls.user_model.create(
            {
                "name": "BA User",
                "login": "ba_user_sequence_setup",
                "email": "ba_user_sequence_setup@example.com",
            }
        )
        cls.employee_model.create(
            {
                "name": "BA User",
                "user_id": cls.user.id,
                "department_id": cls.department.id,
            }
        )

        cls.project = cls.project_model.create(
            {
                "name": "Project BA",
                "job_type": "job",
                "project_department_id": cls.department.id,
                "job_no": "JOB-BA-0001",
            }
        )
        cls.category = cls.category_model.create({"name": "Implementation"})
        cls.site = cls.site_model.create(
            {
                "name": "https://example.test",
                "project_id": cls.project.id,
            }
        )
        cls.database = cls.db_model.create(
            {
                "name": "TESTDB",
                "project_site_id": cls.site.id,
            }
        )

    def test_action_create_task_sequence_builds_monthly_sequence(self):
        self.department.action_create_task_sequence()
        sequence = self.department.project_task_sequence_id

        self.assertTrue(
            sequence, "Department should receive a generated task sequence."
        )
        self.assertEqual(sequence.padding, 5)
        self.assertTrue(sequence.use_date_range)
        self.assertEqual(sequence.prefix, "BA%(range_month)s%(range_y)s-")

    def test_sequence_status_marks_ready_after_generation(self):
        self.department.action_create_task_sequence()
        self.department.invalidate_cache()

        self.assertEqual(
            self.department.task_sequence_status,
            "ready",
            "Department should show ready after a valid task sequence is linked.",
        )
        self.assertTrue(
            self.department.task_sequence_preview.startswith("BA"),
            "Preview should show the department prefix at the start.",
        )

    def test_action_create_task_sequence_rejects_duplicate_creation(self):
        self.department.action_create_task_sequence()

        with self.assertRaisesRegex(
            ValidationError,
            "Please use Refresh Task Sequence",
        ):
            self.department.action_create_task_sequence()

    def test_task_creation_uses_department_selected_sequence(self):
        self.department.action_create_task_sequence()

        task = self.task_model.with_user(self.user).create(
            {
                "name": "Create BA task",
                "project_id": self.project.id,
                "task_category_id": self.category.id,
                "project_site_id": self.site.id,
                "project_site_database_ids": [(6, 0, [self.database.id])],
                "user_id": self.user.id,
            }
        )

        self.assertRegex(task.code, r"^BA\d{4}-\d{5}$")
        self.assertEqual(
            task.display_name,
            "[%s/%s] %s" % (task.code, self.project.job_no, task.name),
        )
        self.assertEqual(
            task.name_get()[0][1],
            "[%s/%s] %s" % (task.code, self.project.job_no, task.name),
        )

    def test_task_creation_explains_department_setup_when_sequence_missing(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Please complete Department Sequence Setup first.",
        ):
            self.task_model.with_user(self.user).create(
                {
                    "name": "Task without setup",
                    "project_id": self.project.id,
                    "task_category_id": self.category.id,
                    "project_site_id": self.site.id,
                    "project_site_database_ids": [(6, 0, [self.database.id])],
                    "user_id": self.user.id,
                }
            )

    def test_task_creation_rejects_invalid_department_sequence_setup(self):
        self.department.action_create_task_sequence()
        self.department.project_task_sequence_id.sudo().write(
            {"prefix": "WRONG%(range_month)s%(range_y)s-"}
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Department Sequence Setup is invalid.",
        ):
            self.task_model.with_user(self.user).create(
                {
                    "name": "Task with invalid setup",
                    "project_id": self.project.id,
                    "task_category_id": self.category.id,
                    "project_site_id": self.site.id,
                    "project_site_database_ids": [(6, 0, [self.database.id])],
                    "user_id": self.user.id,
                }
            )

    def test_department_form_exposes_setup_buttons_and_fields(self):
        result = self.department_model.fields_view_get(view_type="form")
        doc = etree.fromstring(result["arch"].encode())

        self.assertTrue(doc.xpath("//field[@name='task_code_prefix']"))
        self.assertTrue(doc.xpath("//field[@name='project_task_sequence_id']"))
        self.assertTrue(doc.xpath("//field[@name='task_sequence_status']"))
        self.assertTrue(doc.xpath("//field[@name='task_sequence_preview']"))
        self.assertTrue(doc.xpath("//button[@name='action_create_task_sequence']"))
        self.assertTrue(doc.xpath("//button[@name='action_refresh_task_sequence']"))

    def test_department_form_shows_only_valid_action_by_sequence_state(self):
        result_before = self.department_model.fields_view_get(view_type="form")
        doc_before = etree.fromstring(result_before["arch"].encode())

        create_buttons_before = doc_before.xpath(
            "//button[@name='action_create_task_sequence']"
        )
        refresh_buttons_before = doc_before.xpath(
            "//button[@name='action_refresh_task_sequence']"
        )

        self.assertTrue(create_buttons_before)
        self.assertTrue(refresh_buttons_before)
        self.assertIn("project_task_sequence_id", create_buttons_before[0].get("attrs", ""))
        self.assertIn(
            "project_task_sequence_id",
            refresh_buttons_before[0].get("attrs", ""),
        )

        self.department.action_create_task_sequence()
        result_after = self.department_model.fields_view_get(view_type="form")
        doc_after = etree.fromstring(result_after["arch"].encode())
        create_buttons_after = doc_after.xpath(
            "//button[@name='action_create_task_sequence']"
        )
        refresh_buttons_after = doc_after.xpath(
            "//button[@name='action_refresh_task_sequence']"
        )

        self.assertTrue(create_buttons_after)
        self.assertTrue(refresh_buttons_after)
