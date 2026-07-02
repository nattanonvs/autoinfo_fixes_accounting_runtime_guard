from odoo import fields, models


class KnowledgeAttachment(models.Model):
    _name = "knowledge.attachment"
    _description = "Knowledge Attachment"
    _order = "sequence, id"

    knowledge_item_id = fields.Many2one(
        "knowledge.item", required=True, ondelete="cascade"
    )
    attachment_id = fields.Many2one("ir.attachment", required=True, ondelete="cascade")
    source_type = fields.Selection(
        [
            ("upload", "Upload"),
            ("scan", "Scan"),
            ("generated", "Generated"),
        ],
        default="upload",
        required=True,
    )
    uploaded_by = fields.Many2one(
        "res.users", default=lambda self: self.env.user, required=True
    )
    visibility = fields.Selection(
        [
            ("knowledge", "Knowledge"),
            ("internal_only", "Internal Only"),
        ],
        default="knowledge",
        required=True,
    )
    sequence = fields.Integer(default=10)
