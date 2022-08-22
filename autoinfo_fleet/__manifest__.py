# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Fleet',
    'version': '1.0',
    'category': 'DTR - ERP Fleet',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Extends the functionality of Fleet',
    'description': """
Description
-----------
Extends the functionality of Fleet.

Changelog
---------

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': ['fleet', 'base'],
    'application': False,
    'data': [
        'data/email_template.xml',
        'data/auto_job.xml',
        'views/res_config_settings_view.xml',
        'views/fleet_vehicle_view.xml'
    ],
}
