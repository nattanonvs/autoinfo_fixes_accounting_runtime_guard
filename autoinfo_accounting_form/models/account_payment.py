# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    autoinfo_remark = fields.Text(string='Remark (Report)')
