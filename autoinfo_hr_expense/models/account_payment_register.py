from odoo import api, Command, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    wht_ids = fields.Many2many('dtr.wht', 'account_payment_register_wht_rel', string='Withholding Taxes')
