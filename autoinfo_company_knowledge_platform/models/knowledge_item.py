from odoo import api, fields, models
from odoo.exceptions import AccessError


class KnowledgeItem(models.Model):
    _name = "knowledge.item"
    _description = "Knowledge Item"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    ALLOWED_CLEARANCE = {
        "public": ["public", "internal", "restricted", "confidential"],
        "internal": ["internal", "restricted", "confidential"],
        "restricted": ["restricted", "confidential"],
        "confidential": ["confidential"],
    }

    name = fields.Char(
        default=lambda self: self.env["ir.sequence"].next_by_code("knowledge.item"),
        required=True,
        copy=False,
        tracking=True,
    )
    title = fields.Char(required=True, tracking=True)
    summary = fields.Text(required=True)
    body = fields.Html()
    department_id = fields.Many2one(
        "knowledge.department", required=True, tracking=True
    )
    knowledge_type_id = fields.Many2one(
        "knowledge.type", required=True, tracking=True
    )
    tag_ids = fields.Many2many("knowledge.tag", string="Tags")
    owner_id = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user, tracking=True
    )
    contributor_ids = fields.Many2many(
        "res.users", "knowledge_item_contributor_rel", "item_id", "user_id"
    )
    reviewer_id = fields.Many2one("res.users")
    approver_id = fields.Many2one("res.users")
    effective_date = fields.Date()
    review_due_date = fields.Date()
    is_company_wide = fields.Boolean(default=False)
    classification = fields.Selection(
        [
            ("public", "Public"),
            ("internal", "Internal"),
            ("restricted", "Restricted"),
            ("confidential", "Confidential"),
        ],
        default="internal",
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_review", "In Review"),
            ("approved", "Approved"),
            ("published", "Published"),
            ("archived", "Archived"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    version_ids = fields.One2many(
        "knowledge.version", "knowledge_item_id", string="Versions"
    )
    current_version_id = fields.Many2one("knowledge.version", copy=False)
    attachment_rel_ids = fields.One2many("knowledge.attachment", "knowledge_item_id")
    extraction_ids = fields.One2many("knowledge.extraction", "knowledge_item_id")

    def _is_knowledge_admin(self, user):
        return user.has_group("base.group_system") or user.has_group(
            "autoinfo_company_knowledge_platform.group_knowledge_admin"
        )

    def _is_reviewer_or_manager(self, user):
        return user.has_group(
            "autoinfo_company_knowledge_platform.group_knowledge_reviewer"
        ) or user.has_group("autoinfo_company_knowledge_platform.group_department_manager")

    def _is_contributor(self, user):
        return user.has_group(
            "autoinfo_company_knowledge_platform.group_knowledge_contributor"
        )

    def write(self, vals):
        user = self.env.user

        if "state" in vals and not self.env.context.get("knowledge_allow_state_write"):
            raise AccessError("State changes must be performed via workflow actions.")

        if not self.env.context.get("knowledge_allow_published_write"):
            if self.filtered(lambda rec: rec.state == "published"):
                raise AccessError("Published knowledge items cannot be edited directly.")

        if self.env.context.get("knowledge_allow_published_write"):
            return super().write(vals)

        if self._is_knowledge_admin(user):
            return super().write(vals)

        if self._is_reviewer_or_manager(user):
            blocked = self.filtered(
                lambda rec: rec.department_id != user.knowledge_department_id
            )
            if blocked:
                raise AccessError(
                    "You may edit knowledge items only within your own department."
                )
            return super().write(vals)

        if self._is_contributor(user):
            blocked = self.filtered(
                lambda rec: rec.owner_id != user or rec.state != "draft"
            )
            if blocked:
                raise AccessError("Contributors may edit only their own draft items.")
            return super().write(vals)

        raise AccessError("You are not allowed to edit knowledge items.")

    def _create_new_version(self, change_summary=None):
        self.ensure_one()
        next_number = max(self.version_ids.mapped("version_number") or [0]) + 1
        version = self.env["knowledge.version"].create(
            {
                "knowledge_item_id": self.id,
                "version_number": next_number,
                "title_snapshot": self.title,
                "body_snapshot": self.body,
                "change_summary": change_summary,
                "state": self.state,
            }
        )
        self.current_version_id = version.id
        return version

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            version = self.env["knowledge.version"].create(
                {
                    "knowledge_item_id": record.id,
                    "version_number": 1,
                    "title_snapshot": record.title,
                    "body_snapshot": record.body,
                    "state": record.state,
                }
            )
            record.with_context(knowledge_allow_published_write=True).write(
                {"current_version_id": version.id}
            )
        return records

    def action_submit_review(self):
        for record in self:
            record.with_context(knowledge_allow_state_write=True).write(
                {"state": "in_review"}
            )
            record._post_workflow_message("Knowledge item submitted for review.")

    def action_publish(self, change_summary=None):
        for record in self:
            record_ctx = record.with_context(
                knowledge_allow_state_write=True, knowledge_allow_published_write=True
            )
            user = record.env.user
            is_admin = user.has_group("base.group_system") or user.has_group(
                "autoinfo_company_knowledge_platform.group_knowledge_admin"
            )
            is_reviewer = user.has_group(
                "autoinfo_company_knowledge_platform.group_knowledge_reviewer"
            )
            is_manager = user.has_group(
                "autoinfo_company_knowledge_platform.group_department_manager"
            )
            same_department = user.knowledge_department_id == record.department_id

            if not is_admin:
                if not ((is_reviewer or is_manager) and same_department):
                    raise AccessError(
                        "You are not allowed to publish this knowledge item."
                    )
                if record.state != "in_review":
                    raise AccessError(
                        "You may publish only items that are in review."
                    )
            record_ctx.write({"state": "published"})
            version = record_ctx._create_new_version(change_summary=change_summary)
            version.write(
                {
                    "state": "published",
                    "approved_by": self.env.user.id,
                    "approved_at": fields.Datetime.now(),
                }
            )
            record._post_workflow_message("Knowledge item published.")

    def _post_workflow_message(self, body):
        self.ensure_one()
        try:
            self.message_post(body=body)
        except Exception:
            return False
        return True

    def action_queue_extraction(self, attachment):
        self.ensure_one()
        source_format = ""
        if attachment.name and "." in attachment.name:
            source_format = attachment.name.rsplit(".", 1)[-1].lower()
        elif attachment.mimetype and "/" in attachment.mimetype:
            source_format = attachment.mimetype.rsplit("/", 1)[-1].lower()
        extraction = self.env["knowledge.extraction"].create(
            {
                "knowledge_item_id": self.id,
                "attachment_id": attachment.id,
                "source_format": source_format,
                "status": "pending",
            }
        )
        return extraction

    def action_open_search(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Knowledge Search",
            "res_model": "knowledge.item",
            "view_mode": "tree,form",
            "domain": [("state", "=", "published")],
            "context": {"search_default_published_only": 1},
        }

    def get_citation_payload(self):
        self.ensure_one()
        return {
            "id": self.id,
            "title": self.title,
            "department": self.department_id.name,
            "classification": self.classification,
            "state": self.state,
        }

    def _user_can_read(self, user):
        self.ensure_one()
        if user.has_group("base.group_system"):
            return True
        if user.has_group("autoinfo_company_knowledge_platform.group_knowledge_admin"):
            return True
        if self.is_company_wide and self.classification in ("public", "internal"):
            return user.knowledge_clearance_level in self.ALLOWED_CLEARANCE[
                self.classification
            ]
        if user.knowledge_department_id != self.department_id:
            return False
        return user.knowledge_clearance_level in self.ALLOWED_CLEARANCE[
            self.classification
        ]

    def check_access_rule(self, operation):
        super().check_access_rule(operation)
        if operation == "read":
            blocked = self.filtered(lambda rec: not rec._user_can_read(self.env.user))
            if blocked:
                raise AccessError(
                    "You do not have permission to read one or more knowledge items."
                )

    def read(self, fields=None, load="_classic_read"):
        if self:
            self.check_access_rule("read")
        return super().read(fields=fields, load=load)
