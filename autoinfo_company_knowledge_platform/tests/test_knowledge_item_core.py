from odoo.tests.common import SavepointCase


class TestKnowledgeItemCore(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["knowledge.department"].create({"name": "Operations"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "SOP"})

    def test_create_knowledge_item_has_default_state_and_sequence(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "Return Goods SOP",
                "summary": "Step-by-step return workflow",
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
            }
        )

        self.assertTrue(item.name)
        self.assertEqual(item.state, "draft")
        self.assertEqual(item.current_version_id.version_number, 1)

    def test_create_knowledge_item_sets_owner_and_initial_version(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "Invoice Submission SOP",
                "summary": "How accounting submits invoices",
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
            }
        )

        self.assertEqual(item.owner_id, self.env.user)
        self.assertEqual(item.version_ids.mapped("version_number"), [1])
        self.assertEqual(
            item.current_version_id.title_snapshot, "Invoice Submission SOP"
        )

    def test_seeded_knowledge_template_data_is_available(self):
        knowledge_type = self.env.ref(
            "autoinfo_company_knowledge_platform.knowledge_type_sop"
        )
        template = self.env.ref(
            "autoinfo_company_knowledge_platform.knowledge_template_sop_default"
        )

        self.assertEqual(knowledge_type.name, "SOP")
        self.assertEqual(template.knowledge_type_id, knowledge_type)
        self.assertTrue(template.body_html)
