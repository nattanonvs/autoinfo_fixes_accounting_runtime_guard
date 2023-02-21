# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os


class DebitNoteForm(models.TransientModel):
    _inherit = 'debit.note.form'

    def show_report(self):
        path = os.path.split(os.path.abspath(__file__))[0]
        file_name = "autoinfo_debit_note_form.jasper"
        self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', file_name)
        return super(DebitNoteForm, self).show_report()

    def get_parameters(self):
        res = super(DebitNoteForm, self).get_parameters()

        res['p_company_en'] = "THE AUTO-INFO CO.,LTD."
        res['p_company_th'] = "บริษัท ออโต้อินโฟ จำกัด"
        res['p_com_address_en'] = "1359 Soi Ladprao 94 (Panjamitr) Ladprao Rd.,Plubpla, Wangthonglang Bangkok 10310, Thailand."
        res['p_com_address_th'] = "1359 ซ.ลาดพร้าว 94 (ปัญจมิตร) ถ.ลาดพร้าว แขวงพลับพลา เขตวังทองหลาง กรุงเทพฯ 10310"
        res['p_com_website'] = "www.auto-info.co.th"
        res['p_remark'] = """- โปรดสั่งจ่ายเช็คขีดคร่อมในนาม บริษัท ออโต้อินโฟ จำกัด <br>- กรุณาโอนเงินเข้าบัญชีธนาคารกสิกรไทย สาขาศรีวรา ทาว์อินทาวน์ เลขที่บัญชี 609-2-00057-3(ออมทรัพย์)<br>- เมื่อพ้นกำหนดชำระเงินแล้ว บริษัทฯ จะคิดดอกเบี้ยในอัตราร้อยละ 1.5% ต่อเดือน<br>- สินค้าตามรายการข้างต้นยังเป็นสิทธิ์ของบริษัท ออโต้อินโฟ จำกัด จนกว่าผู้ซื้อจะชำระสินค้าครบเรียบร้อยแล้ว"""

        return res
