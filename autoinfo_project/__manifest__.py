# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Project',
    'version': '1.0',
    'category': 'DTR - ERP Project',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Extends the functionality of Project',
    'description': """
Description
-----------
Extends the functionality of Project.

Changelog
---------

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['project'],
    'application': False,
    'data': [
        'data/auto_job.xml',
        'data/email_template.xml',
        'views/project_project_view.xml',
        'views/project_task_view.xml'
    ],
}
