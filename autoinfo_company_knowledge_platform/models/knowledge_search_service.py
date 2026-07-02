from odoo import models
import re


class KnowledgeSearchService(models.AbstractModel):
    _name = "knowledge.search.service"
    _description = "Knowledge Search Service"

    def _build_domain(self, query):
        return [("state", "=", "published")]

    def _tokenize(self, text):
        return re.findall(r"\w+", (text or "").lower())

    def _matches_query(self, record, query):
        terms = self._tokenize(query)
        if not terms:
            return False
        haystack = " ".join(
            filter(
                None,
                [
                    record.title or "",
                    record.summary or "",
                    record.body or "",
                    " ".join(
                        filter(
                            None,
                            [
                                text
                                for text in record.extraction_ids.filtered(
                                    lambda rec: rec.status == "success"
                                ).mapped("extracted_text")
                            ],
                        )
                    ),
                ],
            )
        )
        haystack_tokens = set(self._tokenize(haystack))
        return all(term in haystack_tokens for term in terms)

    def search_knowledge(self, query, user, extra_domain=None):
        if not query or not (query or "").strip():
            return self.env["knowledge.item"].browse()
        domain = self._build_domain(query)
        if extra_domain:
            domain += extra_domain
        records = self.env["knowledge.item"].search(
            domain, order="write_date desc, id desc"
        )
        return records.filtered(
            lambda rec: rec._user_can_read(user) and self._matches_query(rec, query)
        )
