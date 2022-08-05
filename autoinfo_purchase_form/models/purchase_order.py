from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    your_ref = fields.Char(string='Your Ref.')
