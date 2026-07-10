{
    "name": "AUTO-INFO : Vendor Bill Deposit PO Reference Fix",
    "version": "15.0.1.0.0",
    "category": "Accounting",
    "summary": "Show PO Reference on vendor bill deposit payment without changing the deposit flow",
    "author": "The Auto-Info Co., Ltd.",
    "website": "https://www.auto-info.co.th",
    "license": "LGPL-3",
    "depends": [
        "account",
        "purchase",
        "dtr_customer_invoices",
        "autoinfo_accounting_form",
        "dtr_deposit_payment",
    ],
    "data": [
        "views/account_move_view.xml",
    ],
    "installable": True,
    "application": False,
}
