# -*- coding: utf-8 -*-
from odoo import models, fields, api
import os


class PoPurchaseRequestReport(models.TransientModel):
    _inherit = 'po.purchase.request.report'

    report_template = fields.Selection([
        ('1', 'Purchase Request Form'),
        ('2', 'Purchase Request Form (FM-PU-04)')], string='Report Template', default='2', required=True)

    def show_report(self):
        if self.report_template == '2':
            path = os.path.split(os.path.abspath(__file__))[0]
            self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', 'po_purchase_request_at_report.jasper')
        return super(PoPurchaseRequestReport, self).show_report()

    def get_parameters(self):
        res = super(PoPurchaseRequestReport, self).get_parameters()
        if self.report_template == '2':
            rpt = self.env.ref('autoinfo_purchase_form.purchase_request_fm_pu_04')
            res['p_ISO'] = rpt.iso_no or ''
            res['p_EName'] = str(rpt.e_name)
            res['p_ESignature'] = str(rpt.e_signature)
            self.name = self.get_file_name(ids, 'purchase.request', 'Purchase Request Form (FM-PU-04)')
        return res
