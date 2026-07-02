from odoo.tests.common import SavepointCase


class TestKnowledgeWorkflow(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["knowledge.department"].create({"name": "Sales"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "FAQ"})
        cls.item = cls.env["knowledge.item"].create(
            {
                "title": "Return FAQ",
                "summary": "Answers for return process",
                "department_id": cls.department.id,
                "knowledge_type_id": cls.knowledge_type.id,
                "classification": "internal",
                "body": "<p>Draft body</p>",
            }
        )

    def test_submit_review_changes_state(self):
        self.item.action_submit_review()
        self.assertEqual(self.item.state, "in_review")

    def test_publish_creates_new_version_snapshot(self):
        self.item.action_submit_review()
        self.item.action_publish(change_summary="Initial publish")
        self.assertEqual(self.item.state, "published")
        self.assertEqual(self.item.current_version_id.change_summary, "Initial publish")
        self.assertEqual(self.item.current_version_id.state, "published")

    def test_publish_posts_chatter_message_without_user_email(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "Chatter Publish",
                "summary": "Test chatter safe post",
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
                "body": "<p>Body</p>",
            }
        )
        item.action_submit_review()
        item.action_publish(change_summary="Publish")
        self.assertTrue(item.message_ids)
