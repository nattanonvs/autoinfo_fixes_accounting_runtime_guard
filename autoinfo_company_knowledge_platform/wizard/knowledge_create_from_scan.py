from odoo import fields, models
from odoo.exceptions import AccessError


class KnowledgeCreateFromScan(models.TransientModel):
    _name = "knowledge.create.from.scan"
    _description = "Create Knowledge From Scan"

    title = fields.Char(required=True)
    summary = fields.Text(required=True)
    department_id = fields.Many2one("knowledge.department", required=True)
    knowledge_type_id = fields.Many2one("knowledge.type", required=True)
    classification = fields.Selection(
        [
            ("public", "Public"),
            ("internal", "Internal"),
            ("restricted", "Restricted"),
            ("confidential", "Confidential"),
        ],
        default="internal",
        required=True,
    )
    scan_file = fields.Binary(required=True)
    scan_filename = fields.Char(required=True)

    def action_create(self):
        self.ensure_one()
        user = self.env.user
        is_admin = user.has_group("base.group_system") or user.has_group(
            "autoinfo_company_knowledge_platform.group_knowledge_admin"
        )
        if not is_admin:
            if not user.knowledge_department_id or self.department_id != user.knowledge_department_id:
                raise AccessError(
                    "You may create scan knowledge items only for your own department."
                )
        item = self.env["knowledge.item"].create(
            {
                "title": self.title,
                "summary": self.summary,
                "department_id": self.department_id.id,
                "knowledge_type_id": self.knowledge_type_id.id,
                "classification": self.classification,
            }
        )
        attachment = self.env["ir.attachment"].create(
            {
                "name": self.scan_filename,
                "type": "binary",
                "datas": self.scan_file,
                "res_model": "knowledge.item",
                "res_id": item.id,
            }
        )
        self.env["knowledge.attachment"].create(
            {
                "knowledge_item_id": item.id,
                "attachment_id": attachment.id,
                "source_type": "scan",
            }
        )
        item.action_queue_extraction(attachment)
        return {
            "type": "ir.actions.act_window",
            "res_model": "knowledge.item",
            "res_id": item.id,
            "view_mode": "form",
            "target": "current",
        }
