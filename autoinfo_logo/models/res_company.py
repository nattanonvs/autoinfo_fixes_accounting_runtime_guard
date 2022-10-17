from odoo import fields, models, api, tools
import os
import base64


class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_iso = fields.Binary(string='Logo ISO', store=True)
