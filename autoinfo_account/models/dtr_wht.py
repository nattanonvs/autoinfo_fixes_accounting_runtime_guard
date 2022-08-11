# -*- coding: utf-8 -*-
from odoo import fields, models, api


class DtrWht(models.Model):
    _inherit = 'dtr.wht'

    def print_form(self):
        self.ensure_one()
        if self.state != 'confirm':
            return False
        else:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/pdf/wht_form?id=%s&copy=False' % (self.id),
                'target': 'new',
            }

    def print_form_without_date(self):
        self.ensure_one()
        if self.state != 'confirm':
            return False
        else:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/pdf/wht_form_without_date?id=%s&copy=False' % (self.id),
                'target': 'new',
            }

    def print_form_copy(self):
        self.ensure_one()
        if self.state != 'confirm':
            return False
        else:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/pdf/wht_form?id=%s&copy=True' % (self.id),
                'target': 'new',
            }

    def print_form_without_date_copy(self):
        self.ensure_one()
        if self.state != 'confirm':
            return False
        else:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/pdf/wht_form_without_date?id=%s&copy=True' % (self.id),
                'target': 'new',
            }