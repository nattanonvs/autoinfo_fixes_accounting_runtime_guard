# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseTradeDiscount(models.TransientModel):
    _inherit = "purchase.trade.discount"

    @api.model
    def _get_current_trade_discount(self):
        if not self.env.context.get('is_pr', False):
            return super(PurchaseTradeDiscount, self)._get_current_trade_discount()
        ids = self.env.context.get('active_id', False)
        pr_id = self.env['purchase.request'].browse(ids)
        return pr_id.trade_discount

    @api.model
    def _get_current_trade_discount_type(self):
        if not self.env.context.get('is_pr', False):
            return super(PurchaseTradeDiscount, self)._get_current_trade_discount_type()
        ids = self.env.context.get('active_id', False)
        pr_id = self.env['purchase.request'].browse(ids)
        return pr_id.trade_discount_type

    trade_discount = fields.Float(string='Trade Discount', store=True, default=_get_current_trade_discount)
    trade_discount_type = fields.Selection([
        ('percent', '%'),
        ('amount', 'Amount'),
    ], string='Discount Type', default=_get_current_trade_discount_type)

    def apply_trade_discount(self):
        if not self.env.context.get('is_pr', False):
            return super(PurchaseTradeDiscount, self).apply_trade_discount()

        ids = self.env.context.get('active_id', False)
        pr_id = self.env['purchase.request'].browse(ids)
        pr_id.write({
            'trade_discount': self.trade_discount,
            'trade_discount_type': self.trade_discount_type
        })
        self.env.cr.commit()

        if not self.product_id:
            vals = self._prepare_trade_discount_product()
            self.product_id = self.env['product.product'].create(vals)
            self.env['ir.config_parameter'].sudo().set_param('dtr_product_master.default_trade_discount_product_id', self.product_id.id)

        for order in self.env['purchase.request'].browse(self._context.get('active_ids', [])):
            if order.trade_discount == 0.0:
                order.line_ids.filtered(lambda line: line.is_trade_discount).unlink()
            else:
                amount = self.trade_discount
                if self.trade_discount_type == 'percent':
                    amount = (self.trade_discount / 100.0) * sum(order.line_ids.filtered(lambda line: not line.is_trade_discount).mapped('price_subtotal'))
                
                trade_discount_line = order.line_ids.filtered(lambda line: line.is_trade_discount)
                if trade_discount_line:
                    trade_discount_line.update({
                        'price_unit': -amount,
                    })
                else:
                    taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                    tax_ids = taxes.ids

                    po_line = self.env['purchase.request.line'].create({
                        'name': self.product_id.name,
                        'price_unit': -amount,
                        'product_qty': 1.0,
                        'request_id': order.id,
                        'product_uom_id': self.product_id.uom_id.id,
                        'product_id': self.product_id.id,
                        'taxes_id': [(6, 0, tax_ids)],
                        'is_trade_discount': True,
                    })
            order._amount_all()

        return {'type': 'ir.actions.act_window_close'}
