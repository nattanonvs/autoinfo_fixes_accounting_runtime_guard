from odoo.tests.common import SavepointCase


class TestKnowledgeIngestion(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["knowledge.department"].create({"name": "HR"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "Policy"})

    def test_create_scan_item_generates_attachment_and_extraction(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "Leave Policy Scan",
                "summary": "Scanned leave policy",
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
            }
        )
        attachment = self.env["ir.attachment"].create(
            {
                "name": "leave_policy.png",
                "type": "binary",
                "datas": "dGVzdA==",
                "res_model": "knowledge.item",
                "res_id": item.id,
            }
        )

        extraction = item.action_queue_extraction(attachment)

        self.assertEqual(extraction.knowledge_item_id, item)
        self.assertEqual(extraction.status, "pending")
        self.assertEqual(extraction.source_format, "png")

    def test_scan_wizard_creates_item_attachment_and_extraction(self):
        wizard = self.env["knowledge.create.from.scan"].create(
            {
                "title": "HR Scan Wizard",
                "summary": "Wizard import",
                "department_id": self.department.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
                "scan_file": "dGVzdA==",
                "scan_filename": "wizard_scan.png",
            }
        )

        action = wizard.action_create()
        item = self.env["knowledge.item"].browse(action["res_id"])

        self.assertEqual(action["res_model"], "knowledge.item")
        self.assertEqual(item.attachment_rel_ids.mapped("source_type"), ["scan"])
        self.assertEqual(item.extraction_ids.mapped("status"), ["pending"])
        self.assertEqual(item.extraction_ids.mapped("source_format"), ["png"])
