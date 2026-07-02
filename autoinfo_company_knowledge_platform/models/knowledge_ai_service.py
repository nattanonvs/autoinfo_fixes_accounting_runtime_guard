from odoo import models
from odoo.tools import html2plaintext


class KnowledgeAiService(models.AbstractModel):
    _name = "knowledge.ai.service"
    _description = "Knowledge AI Answer Service"

    def answer_question(self, question, user):
        if not question or not (question or "").strip():
            return {
                "answer": "Please enter a question.",
                "citations": [],
                "confidence": 0.0,
            }
        candidates = self.env["knowledge.search.service"].search_knowledge(question, user)
        if not candidates:
            return {
                "answer": "No authorized knowledge source matched this question.",
                "citations": [],
                "confidence": 0.0,
            }

        top = candidates[0]
        plain_text = html2plaintext(top.body or "") or ""
        if not plain_text:
            plain_text = top.summary or ""
        if not plain_text:
            extracted = " ".join(
                filter(
                    None,
                    [
                        text
                        for text in top.extraction_ids.filtered(
                            lambda rec: rec.status == "success"
                        ).mapped("extracted_text")
                    ],
                )
            )
            plain_text = extracted or ""
        if not plain_text:
            plain_text = top.title or ""
        summary = plain_text.strip().split(".")[0].strip()
        return {
            "answer": summary,
            "citations": [top.id],
            "confidence": 0.6,
        }
