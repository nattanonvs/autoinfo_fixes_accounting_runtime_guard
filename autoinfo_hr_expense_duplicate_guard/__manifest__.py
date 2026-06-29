{
    "name": "AUTO INFO - HR Expense Duplicate Guard",
    "version": "15.0.1.0.0",
    "category": "AUTO INFO - ERP Expenses",
    "summary": "Prevent duplicate mileage and monthly expense claims",
    "author": "The Auto-Info Co., Ltd.",
    "website": "https://www.dataroot.asia/support-odoo",
    "license": "OPL-1",
    "depends": ["hr_expense", "mail", "analytic"],
    "application": False,
    "data": [
        "security/expense_duplicate_security.xml",
        "security/ir.model.access.csv",
        "data/mail_message_subtype.xml",
        "wizard/hr_expense_duplicate_override_views.xml",
    ],
    "installable": True,
}
