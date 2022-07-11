# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Purchase',
    'version': '1.0',
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

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['autoinfo_project', 'dtr_purchase'],
    'application': False,
    'data': [
        'views/purchase_request_view.xml'
    ],
}
