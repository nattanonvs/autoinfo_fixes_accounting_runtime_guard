# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Purchase Form',
    'version': '1.0',
    'category': 'DTR - ERP Purchase',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Report Purchase.',
    'description': """
Description
-----------
Customize Report Purchase.

Changelog
---------

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['dtr_purchase_form', 'dtr_purchase_project', 'dtr_partner_master', 'product'],
    'application': False,
    'data': [
        'reports/purchase_order_report.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml'
    ],
}
