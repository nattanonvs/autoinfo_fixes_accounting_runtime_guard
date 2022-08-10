# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Account Form',
    'version': '1.2',
    'category': 'DTR - ERP Accounting',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Report Accounting.',
    'description': """
Description
-----------
Customize Report Accounting.
    - Customer invoice Preprint Form (autoinfo)
    - Customer Receipt Preprint Form (autoinfo)

Changelog
---------
**Version 1.2**
    - Fix task A433-T63 ,add Customer Receipt Preprint Form (autoinfo)
    
**Version 1.1**
    - Fix task A433-T63 ,add form Customer invoice Preprint Form (autoinfo)

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': [
        'dtr_accounting_form',
        'autoinfo_employees',
    ],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'reports/autoinfo_tax_invoice_pp_form.xml',
        'reports/autoinfo_receipt_pp_form.xml',
    ],
}
