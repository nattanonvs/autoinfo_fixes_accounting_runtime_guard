# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    cancel_reason = fields.Char(string='Cancel Reason', readonly=True, copy=False)
