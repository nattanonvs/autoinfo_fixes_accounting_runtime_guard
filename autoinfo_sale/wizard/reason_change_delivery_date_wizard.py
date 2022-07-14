# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ReasonChangeDeliveryDateWizard(models.TransientModel):
    _name = 'reason.change.delivery.date.wizard'
    _description = 'Reason Change Delivery Date Wizard'

    sale_order_id = fields.Many2one('sale.order', string='Sala Order', required=True)
    reason = fields.Text(string='Reason', required=True)
    delivery_date = fields.Datetime(string='Delivery Date', required=True)

    def confirm_change_delivery_date(self):
        if self.sale_order_id:
            self.sale_order_id.write({'commitment_date': self.delivery_date, 'reason_change_delivery_date': self.reason})
        return {'type': 'ir.actions.act_window_close'}
