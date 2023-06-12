# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Sale',
    'version': '1.3a',
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

**Version 1.3-1.3a**
    - A21B-T1
    - Set allow field customer reference and customer reference date can edit after approve sale order

**Version 1.2**
    - Auto stamp analytic account from project in sale order

**Version 1.1**
    - Hide field sale_person_no

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['sale', 'stock', 'sale_stock', 'base', 'hr', 'dtr_sales_department', 'dtr_access_right_base', 'dtr_sales', 'sale_tier_validation'],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'security/advance_access_right_security.xml',
        'security/record_rules.xml',
        'wizard/reason_change_delivery_date_wizard.xml',
        'views/sale_order_view.xml',
        'views/res_users_view.xml',
        'views/hr_department_view.xml',
        'views/product_template_view.xml'
    ],
}
