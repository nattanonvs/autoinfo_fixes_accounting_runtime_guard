from odoo import api, fields, models


class AutoinfoRuntimeGuardFixHelp(models.TransientModel):
    _name = "autoinfo.runtime.guard.fix.help"
    _description = "Autoinfo Runtime Guard Fix Help"

    check_id = fields.Many2one(
        "autoinfo.runtime.guard.check",
        required=True,
        readonly=True,
    )
    problem_summary = fields.Char(readonly=True)
    root_cause = fields.Text(readonly=True)
    risk_note = fields.Text(readonly=True)
    fix_steps = fields.Text(readonly=True)
    fix_command = fields.Text(readonly=True)
    verify_command = fields.Text(readonly=True)
    sed_example = fields.Text(readonly=True)
    python_example = fields.Text(readonly=True)

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        check = self.env["autoinfo.runtime.guard.check"].browse(
            self.env.context.get("default_check_id")
        )
        values.update(
            {
                "check_id": check.id,
                "problem_summary": check.summary,
                "root_cause": check.details,
                "risk_note": check.recommended_action,
                "fix_steps": check.recommended_action,
                "fix_command": check.fix_command,
                "verify_command": check.verify_command,
                "sed_example": (
                    check.fix_command
                    if check.fix_command and "sed" in check.fix_command
                    else False
                ),
                "python_example": (
                    "python3 - <<'PY'\n"
                    "print('fill with project-specific manifest patch script')\n"
                    "PY"
                ),
            }
        )
        return values
