# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os
from odoo.exceptions import ValidationError, UserError


class autoinfo_invoice_form(models.TransientModel):
    _name = 'autoinfo.invoice.form'
    _inherit = 'autoinfo.tax.invoice.pp.form'

    type_doc = fields.Selection([('inv_1', 'ใบกำกับภาษี (สินค้า)'), ('inv_2', 'ใบแจ้งหนี้ (บริการ)'), ('inv_3', 'ใบกำกับ / ใบเสร็จรับเงิน(บริการ)')], 'Document Type', required=True, default="inv_1",)



    def show_report(self):
        path = os.path.split(os.path.abspath(__file__))[0]

        if self.type_doc == 'inv_1':
            file_name = "autoinfo_invoice_form.jasper"
        elif self.type_doc == 'inv_2':
            file_name = "autoinfo_invoice_inv2_form.jasper"
        elif self.type_doc == 'inv_3':
            file_name = "autoinfo_invoice_inv3_form.jasper"
        else:
            raise UserError('Please check Document Type again.')

        self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', file_name)
        return super(autoinfo_invoice_form, self).show_report()

    def get_parameters(self):
        res = super(autoinfo_invoice_form, self).get_parameters()

        res['p_company_en'] = "THE AUTO-INFO CO.,LTD."
        res['p_company_th'] = "บริษัท ออโต้อินโฟ จำกัด"
        res['p_com_address_en'] = "1359 Soi Ladprao 94 (Panjamitr) Ladprao Rd.,Plubpla, Wangthonglang Bangkok 10310, Thailand."
        res['p_com_address_th'] = "1359 ซ.ลาดพร้าว 94 (ปัญจมิตร) ถ.ลาดพร้าว แขวงพลับพลา เขตวังทองหลาง กรุงเทพฯ 10310"
        res['p_com_website'] = "www.auto-info.co.th"

        return res
