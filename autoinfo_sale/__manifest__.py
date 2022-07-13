# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Sale',
    'version': '1.0',
    'category': 'DTR - ERP Sale',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Extends the functionality of Sale',
    'description': """
Description
-----------
Extends the functionality of Sale.

Changelog
---------

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['sale', 'stock', 'sale_stock', 'base'],
    'application': False,
    'data': [
        'views/sale_order_view.xml',
        'views/res_users_view.xml'
    ],
}
