# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountMoveInvoiceParentWizard(models.TransientModel):
    _inherit = 'account.move.parent.invoice.wizard'

    def action_save(self):
        res = super(AccountMoveInvoiceParentWizard, self).action_save()
        print ('===============invoice ', self.invoice_id)
        parent_invoice_ids = self.parent_invoice_ids.filtered(lambda x: x.invoice_user_id)
        if parent_invoice_ids:
            self.invoice_id.write({'invoice_user_id': parent_invoice_ids[0].invoice_user_id.id})
        return res
