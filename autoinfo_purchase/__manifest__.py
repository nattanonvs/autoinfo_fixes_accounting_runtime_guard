# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Purchase',
    'version': '1.2b',
    'category': 'DTR - ERP Purchase',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Extends the functionality of Purchase',
    'description': """
Description
-----------
Extends the functionality of Purchase.

Changelog
---------

**Version 1.2-1.2b**
    - Add pr trade discount
    - Auto default analytic account from project to PR lines

**Version 1.1**
    - Add feature running sequence by department in PR and PO

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['autoinfo_project', 'dtr_purchase', 'dtr_purchase_department', 'dtr_analytic_require', 'dtr_product_master',
        'dtr_purchase_discount', 'hr', 'purchase_request', 'purchase', 'account',
    ],
    'application': False,
    'data': [
        'wizard/purchase_trade_discount_view.xml',
        'views/purchase_request_view.xml',
        'views/hr_department_view.xml',
    ],
}
