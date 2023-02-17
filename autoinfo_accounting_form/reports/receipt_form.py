# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os


class ReceiptForm(models.TransientModel):
    _inherit = 'receipt.form'

    def show_report(self):
        path = os.path.split(os.path.abspath(__file__))[0]
        file_name = "autoinfo_receipt_form.jasper"
        self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', file_name)
        return super(ReceiptForm, self).show_report()


    def get_parameters(self):
        res = super(ReceiptForm, self).get_parameters()

        res['p_company_en'] = "THE AUTO-INFO CO.,LTD."
        res['p_company_th'] = "บริษัท ออโต้อินโฟ จำกัด"
        res['p_com_address_en'] = "1359 Soi Ladprao 94 (Panjamitr) Ladprao Rd.,Plubpla, Wangthonglang Bangkok 10310"
        res['p_com_address_th'] = "1359 ซ.ลาดพร้าว 94 (ปัญจมิตร) ถ.ลาดพร้าว แขวงพลับพลา เขตวังทองหลาง กรุงเทพมหานคร 10310"

        return res

