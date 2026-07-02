from odoo import fields, models


class KnowledgeDepartment(models.Model):
    _name = "knowledge.department"
    _description = "Knowledge Department"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
