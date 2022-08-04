# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Employees',
    'version': '1.0',
    'category': 'DTR - ERP Employees',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'DTR - ERP Employees',
    'description': """
Description
-----------
    - Customization Departments (hr.department)

Changelog
---------

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Jirawoot Ak.',
    'depends': ['hr'],
    'application': False,
    'data': [
        'views/hr_department_view.xml',
    ],
}
