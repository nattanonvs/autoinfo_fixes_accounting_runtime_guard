{
    "name": "AUTO-INFO : Fixes Accounting Runtime Guard",
    "version": "15.0.1.0.0",
    "category": "Tools",
    "summary": "Audit runtime blockers and show safe fix guidance for accounting-related Odoo upgrades",
    "author": "The Auto-Info Co., Ltd.",
    "website": "https://www.auto-info.co.th",
    "license": "LGPL-3",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/runtime_guard_views.xml",
        "data/runtime_guard_cron.xml",
    ],
    "installable": True,
    "application": False,
    "created_by": "The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon",
    "credits": [
        "The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon",
        "AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT",
    ],
}
