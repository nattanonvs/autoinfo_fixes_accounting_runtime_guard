# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Inventory Report',
    'version': '1.1',
    'category': 'DTR - ERP Inventory',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Report Inventory.',
    'description': """
Description
-----------
Customize Report Inventory.

Changelog
---------

**Version 1.1**
    - Fixed filter department in report

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['dtr_stock_report'],
    'application': False,
    'data': [
        'reports/inventory_move_report.xml',
        'reports/inventory_valuation_report.xml',
        'reports/inventory_move_special_report.xml',
        'reports/inventory_valuation_special_report.xml',
        'reports/inventory_move_aging_report.xml',
        'reports/inventory_valuation_aging_report.xml'
    ],
}
