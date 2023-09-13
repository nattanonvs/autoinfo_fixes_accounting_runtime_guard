# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Expenses',
    'version': '1.0',
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

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Pracha P.',
    'depends': ['hr_expense', 'dtr_taxation'],
    'application': False,
    'data': [
        'views/account_payment_register_views.xml',
    ],
}
