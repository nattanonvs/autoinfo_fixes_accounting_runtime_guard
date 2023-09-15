from odoo import api, Command, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    wht_ids = fields.Many2many('dtr.wht', 'account_payment_register_wht_rel', string='Withholding Taxes')
    payment_fee_ids = fields.Many2many('dtr.payment.fee', 'account_payment_register_fee_rel', string='Payment Fees')

    def _create_payment_vals_from_wizard(self):
        # OVERRIDE
        payment_vals = super()._create_payment_vals_from_wizard()
        payment_vals.update({
            'payment_wht_ids': [(4, wht.id, None) for wht in self.wht_ids],
            'payment_fee_ids': [(4, fee.id, None) for fee in self.payment_fee_ids],
        })
        return payment_vals
