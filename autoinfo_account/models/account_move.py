# -*- coding: utf-8 -*-
from odoo import fields, models, api

class AutoInfoAccountMove(models.Model):
    _inherit = 'account.move'

    cancel_reason = fields.Char(string='Cancel Reason', readonly=True, copy=False)
    dtr_customer_ref = fields.Char(string='Customer Reference', copy=False)

    def _post(self, soft=True):
        for rec in self.filtered(lambda x: x.name == '/'):
            if rec.dtr_customer_ref:
                rec.write({'name': rec.dtr_customer_ref})
        return super(AutoInfoAccountMove, self)._post(soft)