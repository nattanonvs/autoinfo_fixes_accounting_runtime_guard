# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Expenses',
    'version': '1.0a',
    'category': 'DTR - ERP Expenses',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Expenses',
    'description': """
Description
-----------
    - Customization Expenses

Changelog
---------

**Version 1.0-1.0a**
    - Add Fee, WHT
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Pracha P.',
    'depends': ['hr_expense', 'autoinfo_account',],
    'application': False,
    'data': [
        'views/account_payment_register_views.xml',
    ],
}
