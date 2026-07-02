from odoo import models


class KnowledgeSubmitReview(models.TransientModel):
    _name = "knowledge.submit.review"
    _description = "Submit Knowledge For Review"

    def action_confirm(self):
        record = self.env["knowledge.item"].browse(self.env.context["active_id"])
        record.action_submit_review()
        return {"type": "ir.actions.act_window_close"}
