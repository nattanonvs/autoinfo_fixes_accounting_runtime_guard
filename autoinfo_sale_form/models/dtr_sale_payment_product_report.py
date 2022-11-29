from odoo import fields, models, api


class DtrSalePaymentProductReport(models.Model):
    _name = 'dtr.sale.payment.product.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Payment Product Report'

    name = fields.Text(string='Description', required=True)
