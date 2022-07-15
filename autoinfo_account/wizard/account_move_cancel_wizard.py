# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveCancelWizard(models.TransientModel):
    _name = 'account.move.cancel.wizard'
    _description = 'Account Move Cancel'

    account_move_id = fields.Many2one('account.move', string='Account Move', required=True)
    reason = fields.Text(string='Reason', required=True)

    def confirm_cancel(self):
        if self.account_move_id:
            self.account_move_id.button_cancel()
            self.account_move_id.write({'cancel_reason': self.reason})
        return {'type': 'ir.actions.act_window_close'}
