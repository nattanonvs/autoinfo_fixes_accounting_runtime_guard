# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Account',
    'version': '1.2',
    'category': 'DTR - ERP Accounting',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Extends the functionality of Account',
    'description': """
Description
-----------
Extends the functionality of Account.

Changelog
---------

**Version 1.2**
    - Auto stamp salesperson from parent invoice in credit note and debit note

**Version 1.1**
    - Auto stamp internal note from customer in billing

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['base', 'account', 'purchase_request', 'purchase', 'dtr_taxation', 'dtr_billing', 'dtr_dncn'],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_move_cancel_wizard.xml',
        'views/res_config_settings_view.xml',
        'views/purchase_request_view.xml',
        'views/purchase_order_view.xml',
        'views/account_move_view.xml',
        'views/dtr_wht_view.xml',
        'views/dtr_account_billing_view.xml'
    ],
}
