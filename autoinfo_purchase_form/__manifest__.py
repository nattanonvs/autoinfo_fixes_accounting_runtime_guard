# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Purchase Form',
    'version': '1.15',
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
**Version 1.15**
    - Fix Purchase Order Form (FM-PU-01) (task: A21B-T323)

**Version 1.14-1.14b**
    - Fix task A21B-T194, A21B-T238
    - Fix task A21B-T77 Purchase Order Form

**Version 1.13**
    - Fixed task A21B-T31, A21B-T43, A21B-T50, A21B-T51, A21B-T61, A21B-T77
    - Add (FM-PU-04) Purchase Request Form
    - Fixed task A433-T90, A433-T91, A433-T110, A21B-T7, A21B-T19

**Version 1.12**
    - Fixed task A433-T89, A433-T90

**Version 1.11**
    - Fixed style report from feedback customer

**Version 1.10**
    - Fixed issue display unit price in FM-PU-03

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
    'depends': ['dtr_purchase_form', 'dtr_purchase_project', 'dtr_partner_master', 'dtr_document_sequence_group_purchase',
        'dtr_access_right_base', 'dtr_report_base', 'autoinfo_purchase', 'autoinfo_logo', 'product', 'mail', 'purchase',
    ],
    'application': False,
    'data': [
        'data/form_code.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml',
        'views/dtr_purchase_warranty_report_view.xml',
        'views/dtr_purchase_delivery_to_report_view.xml',
        'views/dtr_purchase_term_report_view.xml',
        'views/dtr_purchase_shipment_report_view.xml',
        'views/dtr_purchase_weight_report_view.xml',
        'views/purchase_request_view.xml',
        'reports/purchase_order_report.xml',
        'reports/po_purchase_request_report.xml',
    ],
}
