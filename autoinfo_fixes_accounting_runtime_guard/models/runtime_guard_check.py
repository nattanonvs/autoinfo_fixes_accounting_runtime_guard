from odoo import fields, models


class AutoinfoRuntimeGuardRun(models.Model):
    _name = "autoinfo.runtime.guard.run"
    _description = "Autoinfo Runtime Guard Run"
    _order = "id desc"

    name = fields.Char(required=True)
    run_scope = fields.Selection(
        [
            ("manual", "Manual"),
            ("scheduled", "Scheduled"),
        ],
        required=True,
        default="manual",
    )
    requested_by = fields.Many2one(
        "res.users",
        default=lambda self: self.env.user,
        readonly=True,
    )
    started_at = fields.Datetime(readonly=True)
    finished_at = fields.Datetime(readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("running", "Running"),
            ("done", "Done"),
            ("failed", "Failed"),
        ],
        default="draft",
        readonly=True,
    )
    check_ids = fields.One2many(
        "autoinfo.runtime.guard.check",
        "run_id",
        string="Checks",
    )
    result_count = fields.Integer(readonly=True)
    warning_count = fields.Integer(readonly=True)
    error_count = fields.Integer(readonly=True)

    def action_run_checks(self):
        for run in self:
            run.write(
                {
                    "state": "running",
                    "started_at": fields.Datetime.now(),
                }
            )
            run.check_ids.unlink()
            results = run._build_v1_results()
            run.env["autoinfo.runtime.guard.check"].create(
                [dict(result, run_id=run.id) for result in results]
            )
            run.write(
                {
                    "state": "done",
                    "finished_at": fields.Datetime.now(),
                    "result_count": len(results),
                    "warning_count": len(
                        [result for result in results if result["severity"] == "warning"]
                    ),
                    "error_count": len(
                        [result for result in results if result["severity"] == "error"]
                    ),
                }
            )
        return True


class AutoinfoRuntimeGuardCheck(models.Model):
    _name = "autoinfo.runtime.guard.check"
    _description = "Autoinfo Runtime Guard Check"
    _order = "severity desc, id desc"

    run_id = fields.Many2one(
        "autoinfo.runtime.guard.run",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(required=True)
    check_code = fields.Char(required=True, index=True)
    category = fields.Selection(
        [
            ("runtime", "Runtime"),
            ("python_package", "Python Package"),
            ("dependency_chain", "Dependency Chain"),
            ("schema_risk", "Schema Risk"),
            ("module_state", "Module State"),
            ("external_db", "External DB"),
        ],
        required=True,
    )
    severity = fields.Selection(
        [
            ("ok", "OK"),
            ("warning", "Warning"),
            ("error", "Error"),
            ("review", "Review"),
        ],
        required=True,
    )
    state = fields.Selection(
        [
            ("ok", "OK"),
            ("warning", "Warning"),
            ("error", "Error"),
            ("review", "Review"),
        ],
        required=True,
    )
    summary = fields.Char(required=True)
    details = fields.Text()
    recommended_action = fields.Text()
    fix_command = fields.Text()
    verify_command = fields.Text()
    is_safe_fix = fields.Boolean(default=False)
    needs_review = fields.Boolean(default=True)
    review_note = fields.Text()
    reviewed_by = fields.Many2one("res.users", readonly=True)
    reviewed_on = fields.Datetime(readonly=True)
    last_run_at = fields.Datetime(
        related="run_id.finished_at",
        readonly=True,
    )

    def action_mark_reviewed(self):
        self.write(
            {
                "state": "review",
                "reviewed_by": self.env.user.id,
                "reviewed_on": fields.Datetime.now(),
            }
        )
        return True

    def action_open_fix_help(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Runtime Guard Fix Help",
            "res_model": "autoinfo.runtime.guard.fix.help",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_check_id": self.id,
            },
        }
