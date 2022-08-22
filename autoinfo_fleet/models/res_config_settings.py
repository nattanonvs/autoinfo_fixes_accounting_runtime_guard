# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    alert_insurance_expired = fields.Integer(string='Alert Insurance Expired Before(days)', default=30, config_parameter='autoinfo_fleet.alert_insurance_expired')
