# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
from odoo.exceptions import ValidationError
import os


class SaleQuotationForm(models.TransientModel):
    _inherit = 'sale.quotation.form'

    def show_report(self):
        ids = self.env.context.get('active_ids')
        for order in self.env['sale.order'].search([('id', 'in', ids)]):
            if not order.order_line:
                raise ValidationError('Quotation no lines.')
        path = os.path.split(os.path.abspath(__file__))[0]
        file_name = "autoinfo_sale_quotation_form.jasper"
        self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', file_name)
        return super(SaleQuotationForm, self).show_report()
