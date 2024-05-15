# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import timedelta


class DtrAccountPrepayment(models.Model):
    _inherit = 'dtr.account.prepayment'

    payment_date = fields.Date(u'Payment Date')
    prepayment_actual_due_date = fields.Date(string='Actual Due Date', compute='_compute_prepayment_actual_due_date', store=True)

    @api.depends('document_date')
    def _compute_prepayment_actual_due_date(self):
    	for rec in self:
    		if rec.document_date:
    			rec.prepayment_actual_due_date = rec.document_date + timedelta(days=30)
    		else:
    			rec.prepayment_actual_due_date = False
