# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Purchase Form',
    'version': '1.5',
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

**Version 1.5**
    - Changed layout display company information
    - Add new field for display in report

**Version 1.4**
    - Add field input for display in purchase order report

**Version 1.3**
    - Changed font and design purchase order report FM-PU-01

**Version 1.2**
    - Changed font and design purchase order report FM-PU-02

**Version 1.1**
    - Changed font and design purchase order report FM-PU-03

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['dtr_purchase_form', 'dtr_purchase_project', 'dtr_partner_master', 'product', 'autoinfo_logo'],
    'application': False,
    'data': [
        'reports/purchase_order_report.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml'
    ],
}
