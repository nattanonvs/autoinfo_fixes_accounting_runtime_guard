# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _default_bot_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('autoinfo_account.bot_url')

    bot_url = fields.Char(string='BOT Url', default=_default_bot_url, readonly=True)
