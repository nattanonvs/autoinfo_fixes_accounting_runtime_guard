from odoo.tests.common import SavepointCase


class TestKnowledgeSearch(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["knowledge.department"].create({"name": "Operations"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "SOP"})
        cls.item = cls.env["knowledge.item"].create(
            {
                "title": "Goods Return Process",
                "summary": "How to receive returned goods",
                "body": "<p>Receive return document and validate warehouse steps.</p>",
                "department_id": cls.department.id,
                "knowledge_type_id": cls.knowledge_type.id,
                "classification": "internal",
            }
        )
        cls.item.action_publish(change_summary="Publish for search")

    def test_keyword_search_returns_published_item(self):
        results = self.env["knowledge.search.service"].search_knowledge(
            "warehouse return", self.env.user
        )

        self.assertIn(self.item, results)

    def test_action_open_search_filters_published_items(self):
        action = self.item.action_open_search()

        self.assertEqual(action["res_model"], "knowledge.item")
        self.assertEqual(action["domain"], [("state", "=", "published")])
        self.assertEqual(action["context"]["search_default_published_only"], 1)

    def test_blank_query_returns_no_results(self):
        results = self.env["knowledge.search.service"].search_knowledge("   ", self.env.user)
        self.assertFalse(results)

    def test_search_matches_ocr_extracted_text(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "OCR Only",
                "summary": "No body",
                "body": False,
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
            }
        )
        item.action_publish(change_summary="Publish OCR")

        attachment = self.env["ir.attachment"].create(
            {
                "name": "ocr.pdf",
                "type": "binary",
                "datas": "dGVzdA==",
                "res_model": "knowledge.item",
                "res_id": item.id,
            }
        )
        self.env["knowledge.extraction"].create(
            {
                "knowledge_item_id": item.id,
                "attachment_id": attachment.id,
                "status": "success",
                "extracted_text": "Warehouse return steps from OCR",
            }
        )

        results = self.env["knowledge.search.service"].search_knowledge(
            "warehouse return", self.env.user
        )
        self.assertIn(item, results)
