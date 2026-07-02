from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestKnowledgeScanWizardAcl(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["knowledge.department"].create({"name": "Ops"})
        cls.other_department = cls.env["knowledge.department"].create({"name": "Other"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "Policy"})

        base_user_group = cls.env.ref("base.group_user")
        contributor_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_knowledge_contributor"
        )
        cls.user_contributor = cls.env["res.users"].create(
            {
                "name": "Contributor Scan",
                "login": "contributor_scan",
                "groups_id": [(6, 0, [base_user_group.id, contributor_group.id])],
                "knowledge_department_id": cls.department.id,
                "knowledge_clearance_level": "internal",
            }
        )

    def test_contributor_can_use_scan_wizard(self):
        wizard = (
            self.env["knowledge.create.from.scan"]
            .with_user(self.user_contributor)
            .create(
                {
                    "title": "Contributor Scan",
                    "summary": "Scan by contributor",
                    "department_id": self.department.id,
                    "knowledge_type_id": self.knowledge_type.id,
                    "classification": "internal",
                    "scan_file": "dGVzdA==",
                    "scan_filename": "scan.png",
                }
            )
        )
        action = wizard.action_create()
        item = self.env["knowledge.item"].browse(action["res_id"])
        self.assertEqual(action["res_model"], "knowledge.item")
        self.assertEqual(item.department_id, self.department)

    def test_contributor_cannot_create_scan_item_for_other_department(self):
        wizard = (
            self.env["knowledge.create.from.scan"]
            .with_user(self.user_contributor)
            .create(
                {
                    "title": "Contributor Scan Other",
                    "summary": "Scan by contributor",
                    "department_id": self.other_department.id,
                    "knowledge_type_id": self.knowledge_type.id,
                    "classification": "internal",
                    "scan_file": "dGVzdA==",
                    "scan_filename": "scan.png",
                }
            )
        )
        with self.assertRaises(AccessError):
            wizard.action_create()
