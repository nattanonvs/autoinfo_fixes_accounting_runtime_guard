import importlib

from odoo import models


class AutoinfoRuntimeGuardRunService(models.Model):
    _inherit = "autoinfo.runtime.guard.run"

    def _build_v1_results(self):
        self.ensure_one()
        results = []
        results.extend(self._build_runtime_path_results())
        results.extend(self._build_python_package_results())
        results.extend(self._build_dependency_chain_results())
        results.extend(self._build_schema_risk_results())
        results.extend(self._build_module_state_results())
        results.extend(self._build_external_db_warning_results())
        return results

    def _build_runtime_path_results(self):
        expected = "python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf"
        return [
            {
                "name": "Runtime Path",
                "check_code": "runtime_path",
                "category": "runtime",
                "severity": "ok",
                "state": "ok",
                "summary": "Expected Linux runtime command is documented",
                "details": expected,
                "recommended_action": "Use the verified runtime path in deployment docs and support guidance.",
                "fix_command": False,
                "verify_command": "python3 /var/odoo/odoo15/odoo-bin --version",
                "is_safe_fix": False,
                "needs_review": False,
            }
        ]

    def _get_python_package_statuses(self):
        package_map = {
            "PyPDF2": "PyPDF2",
            "Pillow": "PIL",
            "reportlab": "reportlab",
            "Babel": "babel",
            "passlib": "passlib",
            "pdfminer.six": "pdfminer",
        }
        statuses = []
        for display_name, import_name in package_map.items():
            try:
                importlib.import_module(import_name)
                statuses.append((display_name, True))
            except ImportError:
                statuses.append((display_name, False))
        return statuses

    def _build_python_package_results(self):
        results = []
        for display_name, is_installed in self._get_python_package_statuses():
            verify_import = "PIL" if display_name == "Pillow" else display_name.replace(
                ".six", ""
            )
            results.append(
                {
                    "name": "%s Package" % display_name,
                    "check_code": "python_package_%s"
                    % display_name.lower().replace(".", "_"),
                    "category": "python_package",
                    "severity": "ok" if is_installed else "error",
                    "state": "ok" if is_installed else "error",
                    "summary": "%s is %s"
                    % (display_name, "available" if is_installed else "missing"),
                    "details": "Import check for %s" % display_name,
                    "recommended_action": (
                        "Install into the same Python interpreter used by Odoo."
                        if not is_installed
                        else "No action required."
                    ),
                    "fix_command": (
                        False
                        if is_installed
                        else "python3 -m pip install %s" % display_name
                    ),
                    "verify_command": "python3 -c \"import %s\"" % verify_import,
                    "is_safe_fix": False,
                    "needs_review": not is_installed,
                }
            )
        return results

    def _find_dependency_chain_risks(self):
        return []

    def _build_dependency_chain_results(self):
        results = []
        for risk in self._find_dependency_chain_risks():
            results.append(
                {
                    "name": "Dependency Chain Risk",
                    "check_code": "dependency_chain_%s" % risk["module_name"],
                    "category": "dependency_chain",
                    "severity": "error",
                    "state": "error",
                    "summary": "Field %s may load without required dependency"
                    % risk["field_name"],
                    "details": "Module %s appears to need %s"
                    % (risk["module_name"], risk["missing_dependency"]),
                    "recommended_action": "Add the missing dependency in the source module manifest and rerun upgrade.",
                    "fix_command": "sed -i \"s/'depends': \\[/'depends': ['%s', /\" /var/odoo/%s/__manifest__.py"
                    % (risk["missing_dependency"], risk["module_name"]),
                    "verify_command": "grep -n \"%s\" /var/odoo/%s/__manifest__.py"
                    % (risk["missing_dependency"], risk["module_name"]),
                    "is_safe_fix": False,
                    "needs_review": True,
                }
            )
        return results

    def _detect_schema_risks(self):
        return []

    def _build_schema_risk_results(self):
        results = []
        for risk in self._detect_schema_risks():
            results.append(
                {
                    "name": "Schema Risk",
                    "check_code": "schema_risk_%s_%s"
                    % (risk["model"].replace(".", "_"), risk["field"]),
                    "category": "schema_risk",
                    "severity": "error",
                    "state": "error",
                    "summary": "Field %s missing from %s"
                    % (risk["field"], risk["model"]),
                    "details": "Root cause hint: %s" % risk["root_cause"],
                    "recommended_action": "Upgrade the missing dependency chain before retrying the business module.",
                    "fix_command": False,
                    "verify_command": "Check module dependency and rerun upgrade for the owning module.",
                    "is_safe_fix": False,
                    "needs_review": True,
                }
            )
        return results

    def _get_modules_to_upgrade(self):
        return self.env["ir.module.module"].search([("state", "=", "to upgrade")]).mapped(
            "name"
        )

    def _build_module_state_results(self):
        module_names = self._get_modules_to_upgrade()
        if not module_names:
            return [
                {
                    "name": "Module Upgrade Backlog",
                    "check_code": "module_state_to_upgrade",
                    "category": "module_state",
                    "severity": "ok",
                    "state": "ok",
                    "summary": "No modules are waiting in to upgrade state",
                    "details": "Backlog is empty",
                    "recommended_action": "No action required.",
                    "fix_command": False,
                    "verify_command": "select string_agg(name, ',') from ir_module_module where state='to upgrade';",
                    "is_safe_fix": False,
                    "needs_review": False,
                }
            ]
        return [
            {
                "name": "Module Upgrade Backlog",
                "check_code": "module_state_to_upgrade",
                "category": "module_state",
                "severity": "warning",
                "state": "warning",
                "summary": "%s modules are still waiting to upgrade" % len(module_names),
                "details": ", ".join(module_names),
                "recommended_action": "Review module order and upgrade them in controlled batches.",
                "fix_command": "select string_agg(name, ',') from ir_module_module where state='to upgrade';",
                "verify_command": "Re-run the SQL and confirm the backlog is empty.",
                "is_safe_fix": False,
                "needs_review": True,
            }
        ]

    def _build_external_db_warning_results(self):
        return [
            {
                "name": "External Database Target",
                "check_code": "external_db_target_warning",
                "category": "external_db",
                "severity": "review",
                "state": "review",
                "summary": "External callers may still target an old database name",
                "details": "Use this record to document old targets such as FROMGOLIVE_15MAR2026 and the correct target such as odoo_golive.",
                "recommended_action": "Coordinate with the integration owner and update client-side connection settings.",
                "fix_command": False,
                "verify_command": "Review integration configuration and access logs.",
                "is_safe_fix": False,
                "needs_review": True,
            }
        ]
