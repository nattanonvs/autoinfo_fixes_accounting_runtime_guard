from odoo import fields, models


class KnowledgeType(models.Model):
    _name = "knowledge.type"
    _description = "Knowledge Type"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
