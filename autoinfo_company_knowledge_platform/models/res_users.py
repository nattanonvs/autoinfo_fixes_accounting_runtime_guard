from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    knowledge_department_id = fields.Many2one("knowledge.department")
    knowledge_clearance_level = fields.Selection(
        [
            ("public", "Public"),
            ("internal", "Internal"),
            ("restricted", "Restricted"),
            ("confidential", "Confidential"),
        ],
        default="internal",
    )
