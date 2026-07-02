from odoo.tests.common import SavepointCase


class TestKnowledgeAiAnswer(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["knowledge.department"].create(
            {"name": "Customer Service"}
        )
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "SOP"})
        cls.item = cls.env["knowledge.item"].create(
            {
                "title": "VIP Refund SOP",
                "summary": "How to process VIP refund",
                "body": "<p>Review refund eligibility, get manager approval, and notify finance.</p>",
                "department_id": cls.department.id,
                "knowledge_type_id": cls.knowledge_type.id,
                "classification": "internal",
            }
        )
        cls.item.action_publish(change_summary="Published for AI")

    def test_ai_answer_returns_summary_and_citation(self):
        answer = self.env["knowledge.ai.service"].answer_question(
            "How to process VIP refund?", self.env.user
        )

        self.assertIn("manager approval", answer["answer"])
        self.assertEqual(answer["citations"], [self.item.id])
        self.assertEqual(
            self.item.get_citation_payload()["department"], "Customer Service"
        )

    def test_ai_answer_returns_no_source_message_when_no_match(self):
        answer = self.env["knowledge.ai.service"].answer_question(
            "unknown process question", self.env.user
        )

        self.assertEqual(answer["citations"], [])
        self.assertEqual(answer["confidence"], 0.0)

    def test_ai_answer_rejects_blank_question(self):
        answer = self.env["knowledge.ai.service"].answer_question("   ", self.env.user)
        self.assertEqual(answer["citations"], [])
        self.assertEqual(answer["confidence"], 0.0)

    def test_ai_answer_can_use_ocr_text(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "OCR Answer",
                "summary": "",
                "body": False,
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
            }
        )
        item.action_publish(change_summary="Publish OCR answer")

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
                "extracted_text": "Step one: get manager approval. Step two: notify finance.",
            }
        )

        answer = self.env["knowledge.ai.service"].answer_question(
            "manager approval", self.env.user
        )
        self.assertIn("manager approval", answer["answer"])
        self.assertEqual(answer["citations"], [item.id])
