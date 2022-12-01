# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Purchase Form',
    'version': '1.9',
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

**Version 1.9**
    - Remove require field
    - Add form code for setting jasper report

**Version 1.8**
    - Revised header company information in report

**Version 1.7**
    - Changed font to sarabun (FM-PU-02)

**Version 1.6**
    - Changed font to sarabun (FM-PU-01, FM-PU-03)
    - Add new field for purchase order report (FM-PU-01, FM-PU-03)
    - Add field list price in purchase order line and default in price unit

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
    'depends': ['dtr_purchase_form', 'dtr_purchase_project', 'dtr_partner_master', 'product', 'autoinfo_logo', 'dtr_access_right_base',
        'mail', 'purchase', 'dtr_report_base'],
    'application': False,
    'data': [
        'data/form_code.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'reports/purchase_order_report.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml',
        'views/dtr_purchase_warranty_report_view.xml',
        'views/dtr_purchase_delivery_to_report_view.xml',
        'views/dtr_purchase_term_report_view.xml',
        'views/dtr_purchase_shipment_report_view.xml',
        'views/dtr_purchase_weight_report_view.xml'
    ],
}
