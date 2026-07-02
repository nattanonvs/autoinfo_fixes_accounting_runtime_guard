from odoo import fields, models


class KnowledgeTag(models.Model):
    _name = "knowledge.tag"
    _description = "Knowledge Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=0)
