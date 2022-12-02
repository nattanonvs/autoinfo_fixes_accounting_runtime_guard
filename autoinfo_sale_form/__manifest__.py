# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Sales Form',
    'version': '1.8',
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

**Version 1.8**
    - Resize height of textbox in quotation report

**Version 1.7**
    - Revised header company information in report
    - Add new field project name for display in report

**Version 1.6**
    - Changed font to sarabun and add new field in quotation report

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
    'depends': ['dtr_sales_form', 'sale', 'autoinfo_logo', 'dtr_access_right_sales', 'mail', 'base'],
    'application': False,
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/sale_order_view.xml',
        'views/dtr_sale_price_report_view.xml',
        'views/dtr_sale_delivery_report_view.xml',
        'views/dtr_sale_payment_product_report_view.xml',
        'views/dtr_sale_payment_engineering_report_view.xml',
        'views/dtr_sale_validity_report_view.xml',
        'views/dtr_sale_warranty_report_view.xml',
        'views/dtr_sale_credit_report_view.xml'
    ],
}
