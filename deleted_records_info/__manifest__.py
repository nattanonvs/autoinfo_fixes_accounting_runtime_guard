# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.
# Author: Aktiv Software PVT. LTD.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#    Aktiv Software:
#          - Chirag Patel
#          - Harsh Tanna
#          - Harshil Soni
{
    "name": "Track Deleted Records",
    "summary": """
        View deleted records.""",
    "description": """
    This module helps Admin users to see which records have been deleted and by whom.
    """,
    "author": "Aktiv Software",
    "website": "http://www.aktivsoftware.com",
    "category": "Extra Tools",
    "version": "15.0.1.0.0",
     "license": "OPL-1",
    "price": 10.00,
    "currency": "USD",
    "depends": ["base_setup"],
    "data": [
        "security/deleted_records_security.xml",
        "security/ir.model.access.csv",
        "views/deleted_records_views.xml",
        "wizard/delete_records_upto_wizard_views.xml",
    ],
    "external_dependencies": {"python": ["pyscreenshot"]},
    "images": ["static/description/banner.jpg"],
    "auto_install": False,
    "installable": True,
    "application": False,
}
