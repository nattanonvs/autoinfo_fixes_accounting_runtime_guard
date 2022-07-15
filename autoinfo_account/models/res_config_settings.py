# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bot_url = fields.Char(string='BOT URL', config_parameter='autoinfo_account.bot_url')
