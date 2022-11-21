# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Sales Form',
    'version': '1.5',
    'category': 'DTR - ERP Sales',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Report Sales.',
    'description': """
Description
-----------
Customize Report Sales.

Changelog
---------

**Version 1.5**
    - Changed layout display company information

**Version 1.4**
    - Add sale person name, position and signature in footer quotation report

**Version 1.3**
    - Add require field in sale order

**Version 1.2**
    - Display warranty in quotation report

**Version 1.1**
    - Changed font and design quotation report

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['dtr_sales_form', 'sale', 'autoinfo_logo'],
    'application': False,
    'data': [
        'views/sale_order_view.xml'
    ],
}
