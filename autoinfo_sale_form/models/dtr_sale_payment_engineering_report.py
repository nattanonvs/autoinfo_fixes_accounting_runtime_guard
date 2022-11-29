from odoo import fields, models, api


class DtrSalePaymentEngineeringReport(models.Model):
    _name = 'dtr.sale.payment.engineering.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Payment Engineering Report'

    name = fields.Text(string='Description', required=True)
