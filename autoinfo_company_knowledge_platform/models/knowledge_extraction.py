from odoo import fields, models


class KnowledgeExtraction(models.Model):
    _name = "knowledge.extraction"
    _description = "Knowledge Extraction"
    _order = "id desc"

    knowledge_item_id = fields.Many2one(
        "knowledge.item", required=True, ondelete="cascade"
    )
    attachment_id = fields.Many2one("ir.attachment", required=True, ondelete="cascade")
    source_format = fields.Char()
    extracted_text = fields.Text()
    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("success", "Success"),
            ("failed", "Failed"),
        ],
        default="pending",
        required=True,
    )
    confidence_score = fields.Float(default=0.0)
    error_message = fields.Char()
    processed_at = fields.Datetime()
