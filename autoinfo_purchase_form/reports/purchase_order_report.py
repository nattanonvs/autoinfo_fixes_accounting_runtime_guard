# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os


class PurchaseOrderReport(models.TransientModel):
    _inherit = 'purchase.order.report'

    report_template = fields.Selection([
        ('1', 'ใบสั่งซื้อสั่งจ้าง (PURCHASE ORDER) FM-PU-01'),
        ('2', 'PURCHASE ORDER (INDENT IA BA)  FM-PU-02'),
        ('3', 'PURCHASE ORDER (INDENT TA ) FM-PU-03')], string='Report Template', default='1', required=True)

    def show_report(self):
        path = os.path.split(os.path.abspath(__file__))[0]
        if self.report_template == '1':
            file_name = 'autoinfo_purchase_order_form1.jasper'
        elif self.report_template == '2':
            file_name = 'autoinfo_purchase_order_form2.jasper'
        else:
            file_name = 'autoinfo_purchase_order_form3.jasper'
            
        self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', file_name)
        return super(PurchaseOrderReport, self).show_report()

    def get_parameters(self):
        res = super(PurchaseOrderReport, self).get_parameters()
        if self.report_template == '2':
            self.name = 'PURCHASE ORDER (INDENT IA BA)  FM-PU-02'
        elif self.report_template == '3':
            self.name = 'PURCHASE ORDER (INDENT TA ) FM-PU-03'
        return res
