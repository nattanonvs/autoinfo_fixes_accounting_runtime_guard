# -*- coding: utf-8 -*-
from odoo import fields, models, api


class DtrAccountPrepayment(models.Model):
    _inherit = 'dtr.account.prepayment'

    payment_date = fields.Date(u'Payment Date')
