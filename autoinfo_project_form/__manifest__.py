# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Project Form',
    'version': '1.0',
    'category': 'DTR - ERP Project',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Report Project.',
    'description': """
Description
-----------
Customize Report Project.

Changelog
---------

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['project', 'dtr_jasper', 'dtr_report_base', 'base'],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'data/form_code.xml',
        'reports/autoinfo_job_assignment_document_form.xml',
        'views/project_project_view.xml'
    ],
}
