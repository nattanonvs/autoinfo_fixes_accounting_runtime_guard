from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrDepartment(models.Model):
    _inherit = "hr.department"

    task_code_prefix = fields.Char(string="Task Code Prefix")
    project_no_job_sequence_id = fields.Many2one(
        "ir.sequence", string="Project Job No.(Job) Sequence", check_company=True
    )
    project_no_pm_sequence_id = fields.Many2one(
        "ir.sequence", string="Project Job No.(PM) Sequence", check_company=True
    )
    project_no_service_sequence_id = fields.Many2one(
        "ir.sequence", string="Project Job No.(Service) Sequence", check_company=True
    )
    project_task_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Task Sequence",
        check_company=True,
        domain="[('active', '=', True)]",
    )
    task_sequence_status = fields.Selection(
        [
            ("not_configured", "Not Configured"),
            ("invalid", "Invalid Setup"),
            ("ready", "Ready"),
        ],
        string="Task Sequence Status",
        compute="_compute_task_sequence_setup",
    )
    task_sequence_preview = fields.Char(
        string="Task Sequence Preview",
        compute="_compute_task_sequence_setup",
    )

    @api.depends(
        "task_code_prefix",
        "project_task_sequence_id",
        "project_task_sequence_id.prefix",
        "project_task_sequence_id.padding",
        "project_task_sequence_id.use_date_range",
        "project_task_sequence_id.active",
    )
    def _compute_task_sequence_setup(self):
        today = fields.Date.today()
        month_start = today.replace(day=1)
        for department in self:
            sequence = department.project_task_sequence_id
            if not department.task_code_prefix or not sequence:
                department.task_sequence_status = "not_configured"
                department.task_sequence_preview = False
                continue
            if department._is_valid_task_sequence(sequence):
                department.task_sequence_status = "ready"
                department.task_sequence_preview = sequence.with_context(
                    ir_sequence_date=today,
                    ir_sequence_date_range=month_start,
                ).get_next_char(1)
            else:
                department.task_sequence_status = "invalid"
                department.task_sequence_preview = False

    def _normalize_task_code_prefix(self):
        self.ensure_one()
        return (self.task_code_prefix or "").strip().upper()

    def _get_expected_task_sequence_prefix(self):
        self.ensure_one()
        return "%s%%(range_month)s%%(range_y)s-" % self._normalize_task_code_prefix()

    def _is_valid_task_sequence(self, sequence):
        self.ensure_one()
        if not sequence or not sequence.active:
            return False
        return (
            bool(self._normalize_task_code_prefix())
            and sequence.padding == 5
            and sequence.use_date_range
            and sequence.prefix == self._get_expected_task_sequence_prefix()
        )

    def _prepare_task_sequence_values(self):
        self.ensure_one()
        prefix = self._normalize_task_code_prefix()
        if not prefix:
            raise ValidationError(_("Please set Task Code Prefix on Department first."))
        return {
            "name": "Task Sequence - %s" % self.name,
            "code": "department.task.%s.%s" % (self.id, prefix.lower()),
            "prefix": "%s%%(range_month)s%%(range_y)s-" % prefix,
            "padding": 5,
            "number_increment": 1,
            "number_next": 1,
            "use_date_range": True,
            "implementation": "standard",
            "company_id": self.company_id.id or False,
        }

    def action_create_task_sequence(self):
        sequence_model = self.env["ir.sequence"].sudo()
        for department in self:
            if department.project_task_sequence_id:
                raise ValidationError(
                    _(
                        "Task Sequence already exists for this Department. "
                        "Please use Refresh Task Sequence instead."
                    )
                )
            values = department._prepare_task_sequence_values()
            sequence = sequence_model.create(values)
            department.write(
                {
                    "task_code_prefix": department._normalize_task_code_prefix(),
                    "project_task_sequence_id": sequence.id,
                }
            )
        return True

    def action_refresh_task_sequence(self):
        for department in self:
            if not department.project_task_sequence_id:
                raise ValidationError(
                    _("Please select Task Sequence on Department first.")
                )
            values = department._prepare_task_sequence_values()
            department.project_task_sequence_id.sudo().write(
                {
                    "name": values["name"],
                    "code": values["code"],
                    "prefix": values["prefix"],
                    "padding": values["padding"],
                    "number_increment": values["number_increment"],
                    "use_date_range": values["use_date_range"],
                    "implementation": values["implementation"],
                    "company_id": values["company_id"],
                }
            )
            department.task_code_prefix = department._normalize_task_code_prefix()
        return True

    @api.constrains("task_code_prefix", "project_task_sequence_id")
    def _check_task_sequence_setup(self):
        for department in self.filtered("project_task_sequence_id"):
            if not department._is_valid_task_sequence(department.project_task_sequence_id):
                raise ValidationError(
                    _(
                        "Task Sequence must be active, use monthly date ranges, "
                        "use padding 5, and match the Department prefix."
                    )
                )
