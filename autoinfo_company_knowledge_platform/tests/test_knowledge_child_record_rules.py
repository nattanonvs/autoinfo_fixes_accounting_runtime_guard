from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestKnowledgeChildRecordRules(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sales = cls.env["knowledge.department"].create({"name": "Sales"})
        cls.finance = cls.env["knowledge.department"].create({"name": "Finance"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "Policy"})

        base_user_group = cls.env.ref("base.group_user")
        contributor_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_knowledge_contributor"
        )

        cls.user_sales_contributor = cls.env["res.users"].create(
            {
                "name": "Sales Contributor",
                "login": "sales_contributor_child",
                "groups_id": [(6, 0, [base_user_group.id, contributor_group.id])],
                "knowledge_department_id": cls.sales.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_finance_contributor = cls.env["res.users"].create(
            {
                "name": "Finance Contributor",
                "login": "finance_contributor_child",
                "groups_id": [(6, 0, [base_user_group.id, contributor_group.id])],
                "knowledge_department_id": cls.finance.id,
                "knowledge_clearance_level": "internal",
            }
        )

        cls.finance_item = cls.env["knowledge.item"].create(
            {
                "title": "Finance Restricted",
                "summary": "Restricted finance policy",
                "department_id": cls.finance.id,
                "knowledge_type_id": cls.knowledge_type.id,
                "classification": "restricted",
            }
        )
        cls.finance_item.action_publish(change_summary="Publish finance")

        attachment = cls.env["ir.attachment"].create(
            {
                "name": "finance.pdf",
                "type": "binary",
                "datas": "dGVzdA==",
                "res_model": "knowledge.item",
                "res_id": cls.finance_item.id,
            }
        )
        cls.finance_kattachment = cls.env["knowledge.attachment"].create(
            {
                "knowledge_item_id": cls.finance_item.id,
                "attachment_id": attachment.id,
                "source_type": "upload",
            }
        )
        cls.finance_extraction = cls.env["knowledge.extraction"].create(
            {
                "knowledge_item_id": cls.finance_item.id,
                "attachment_id": attachment.id,
                "status": "success",
                "extracted_text": "Finance confidential process",
            }
        )
        cls.finance_version = cls.finance_item.current_version_id

        cls.sales_item = cls.env["knowledge.item"].create(
            {
                "title": "Sales Internal",
                "summary": "Sales policy",
                "department_id": cls.sales.id,
                "knowledge_type_id": cls.knowledge_type.id,
                "classification": "internal",
            }
        )
        cls.sales_item.action_publish(change_summary="Publish sales")
        cls.sales_version = cls.sales_item.current_version_id

    def test_child_records_blocked_when_parent_not_readable(self):
        with self.assertRaises(AccessError):
            self.finance_version.with_user(self.user_sales_contributor).read(
                ["title_snapshot"]
            )

        with self.assertRaises(AccessError):
            self.finance_kattachment.with_user(self.user_sales_contributor).read(
                ["source_type"]
            )

        with self.assertRaises(AccessError):
            self.finance_extraction.with_user(self.user_sales_contributor).read(
                ["extracted_text"]
            )

    def test_child_records_readable_when_parent_readable(self):
        data = self.sales_version.with_user(self.user_sales_contributor).read(
            ["title_snapshot"]
        )
        self.assertEqual(data[0]["title_snapshot"], "Sales Internal")
