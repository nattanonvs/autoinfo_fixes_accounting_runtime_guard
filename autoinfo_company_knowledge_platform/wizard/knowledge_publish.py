from odoo import fields, models


class KnowledgePublish(models.TransientModel):
    _name = "knowledge.publish"
    _description = "Publish Knowledge"

    change_summary = fields.Char(required=True)

    def action_confirm(self):
        record = self.env["knowledge.item"].browse(self.env.context["active_id"])
        record.action_publish(change_summary=self.change_summary)
        return {"type": "ir.actions.act_window_close"}
