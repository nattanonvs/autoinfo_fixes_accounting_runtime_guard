from odoo import fields, models


class KnowledgeTemplate(models.Model):
    _name = "knowledge.template"
    _description = "Knowledge Template"
    _order = "name"

    name = fields.Char(required=True)
    knowledge_type_id = fields.Many2one("knowledge.type", required=True)
    summary = fields.Text()
    body_html = fields.Html(required=True)
    active = fields.Boolean(default=True)
