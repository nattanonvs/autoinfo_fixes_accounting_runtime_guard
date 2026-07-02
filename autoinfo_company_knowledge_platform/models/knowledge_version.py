from odoo import fields, models


class KnowledgeVersion(models.Model):
    _name = "knowledge.version"
    _description = "Knowledge Version"
    _order = "version_number desc, id desc"

    knowledge_item_id = fields.Many2one(
        "knowledge.item", required=True, ondelete="cascade"
    )
    version_number = fields.Integer(required=True)
    title_snapshot = fields.Char(required=True)
    body_snapshot = fields.Html()
    change_summary = fields.Char()
    created_by = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user
    )
    approved_by = fields.Many2one("res.users")
    approved_at = fields.Datetime()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_review", "In Review"),
            ("approved", "Approved"),
            ("published", "Published"),
            ("archived", "Archived"),
        ],
        default="draft",
        required=True,
    )
