# -*- coding: utf-8 -*-
from odoo import fields, models, api


class DtrAccountBilling(models.Model):
    _inherit = 'dtr.account.billing'

    @api.onchange('partner_id')
    def onchange_billing_partner(self):
        if self.partner_id:
            self.billing_note = self.partner_id.comment
