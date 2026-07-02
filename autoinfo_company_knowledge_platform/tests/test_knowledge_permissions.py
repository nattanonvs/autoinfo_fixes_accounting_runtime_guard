from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestKnowledgePermissions(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sales = cls.env["knowledge.department"].create({"name": "Sales"})
        cls.finance = cls.env["knowledge.department"].create({"name": "Finance"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "Policy"})
        viewer_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_knowledge_viewer"
        )
        base_user_group = cls.env.ref("base.group_user")
        cls.user_sales = cls.env["res.users"].create(
            {
                "name": "Sales User",
                "login": "sales_user",
                "groups_id": [(6, 0, [base_user_group.id, viewer_group.id])],
                "knowledge_department_id": cls.sales.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_finance = cls.env["res.users"].create(
            {
                "name": "Finance User",
                "login": "finance_user",
                "groups_id": [(6, 0, [base_user_group.id, viewer_group.id])],
                "knowledge_department_id": cls.finance.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.item = cls.env["knowledge.item"].create(
            {
                "title": "Finance Policy",
                "summary": "Restricted finance process",
                "department_id": cls.finance.id,
                "knowledge_type_id": cls.knowledge_type.id,
                "classification": "restricted",
                "state": "published",
            }
        )

    def test_user_outside_department_cannot_read_restricted_item(self):
        with self.assertRaises(AccessError):
            self.item.with_user(self.user_sales).read(["title"])

    def test_restricted_item_not_returned_by_search_for_other_department(self):
        results = self.env["knowledge.search.service"].search_knowledge(
            "finance process", self.user_sales
        )

        self.assertNotIn(self.item, results)

    def test_search_read_does_not_raise_and_filters_unauthorized_records(self):
        other_item = self.env["knowledge.item"].create(
            {
                "title": "Sales Policy",
                "summary": "Sales internal policy",
                "department_id": self.sales.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
                "state": "published",
            }
        )

        data = (
            self.env["knowledge.item"]
            .with_user(self.user_sales)
            .search_read([], ["title", "department_id", "classification"])
        )
        ids = [row["id"] for row in data]

        self.assertIn(other_item.id, ids)
        self.assertNotIn(self.item.id, ids)
