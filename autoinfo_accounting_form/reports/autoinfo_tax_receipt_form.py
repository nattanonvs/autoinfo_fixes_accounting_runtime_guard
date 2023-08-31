# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)


class autoinfo_tax_receipt_form(models.TransientModel):

    _name = 'autoinfo.tax.receipt.form'
    _inherit = 'dtr.jasper.report'

    def _compute_default_date_type(self):
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        return rpt.date_type

    def _compute_default_date_format(self):
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        return rpt.date_format

    name = fields.Char('Autoinfo Tax Receipt Form')

    jasper_file = fields.Char(default=lambda self: self.get_jasper_file(__file__))
    p_language = fields.Selection([
        ('thai', u'Thai'),
        ('english', u'English')], 'Document Language', default='thai')

    date_type = fields.Selection([('AD', 'AD'), ('BE', 'BE')], 'Date Type', default=_compute_default_date_type,
                                 help='AD = คริสตศักราช\nBE = พุทธศักราช')
    date_format = fields.Selection([('dd/MM/yy', 'dd/MM/yy'),
        ('dd/MMM/yy', 'dd/MMM/yy'),
        ('MM/dd/yy', 'MM/dd/yy'),
        ('MMM/dd/yy', 'MMM/dd/yy'),
        ('dd/MM/yyyy', 'dd/MM/yyyy'),
        ('dd/MMM/yyyy', 'dd/MMM/yyyy'),
        ('MM/dd/yyyy', 'MM/dd/yyyy'),
        ('MMM/dd/yyyy', 'MMM/dd/yyyy'),
        ('yy/dd/MM', 'yy/dd/MM'),
        ('yy/dd/MMM', 'yy/dd/MMM'),
        ('yy/MM/dd', 'yy/MM/dd'),
        ('yy/MMM/dd', 'yy/MMM/dd'),
        ('yyyy/dd/MM', 'yyyy/dd/MM'),
        ('yyyy/dd/MMM', 'yyyy/dd/MMM'),
        ('yyyy/MM/dd', 'yyyy/MM/dd'),
        ('yyyy/MMM/dd', 'yyyy/MMM/dd'),
        ('dd-MM-yy', 'dd-MM-yy'),
        ('dd-MMM-yy', 'dd-MMM-yy'),
        ('MM-dd-yy', 'MM-dd-yy'),
        ('MMM-dd-yy', 'MMM-dd-yy'),
        ('dd-MM-yyyy', 'dd-MM-yyyy'),
        ('dd-MMM-yyyy', 'dd-MMM-yyyy'),
        ('MM-dd-yyyy', 'MM-dd-yyyy'),
        ('MMM-dd-yyyy', 'MMM-dd-yyyy'),
        ('yy-dd-MM', 'yy-dd-MM'),
        ('yy-dd-MMM', 'yy-dd-MMM'),
        ('yy-MM-dd', 'yy-MM-dd'),
        ('yy-MMM-dd', 'yy-MMM-dd'),
        ('yyyy-dd-MM', 'yyyy-dd-MM'),
        ('yyyy-dd-MMM', 'yyyy-dd-MMM'),
        ('yyyy-MM-dd', 'yyyy-MM-dd'),
        ('yyyy-MMM-dd', 'yyyy-MMM-dd')],
       'Date Format', default=_compute_default_date_format)

    def show_report(self, report_name=False):
        ids = self.env.context.get('active_ids')

        email_subject = 'Tax/Receipt (Autoinfo)'
        email_document_number = ''
        if len(ids) == 1:
            data = self.env['account.payment'].search([('id', 'in', ids)], limit=1)
            email_subject = 'Autoinfo Tax Receipt Form: ' + data.name
            email_document_number = data.name
            self.can_send_email = True

        # Running Line Sequence before Show Report
        for order in self.env['account.payment'].search([('id', 'in', ids)]):
            report_seq = 1
            for line in order.invoice_line_ids:
                if line.display_type and line.display_type == 'line_section':
                    report_seq = 1
                if not line.display_type and not line.is_trade_discount:
                    line.write({
                        'report_sequence': report_seq
                    })
                    report_seq = report_seq + 1

        self.env.cr.commit()
        return super(autoinfo_tax_receipt_form, self).show_report(email_subject=email_subject,
                                                    email_document_number=email_document_number)

    def get_parameters(self):
        ids = self.env.context.get('active_ids')
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        if rpt and not rpt.allow:
            self.err_msg = "Unallow Report"
            raise ValidationError("Unallow Report")
        # self.name = 'Invoice Report'
        self.name = self.get_file_name(ids, 'account.payment', 'Tax Receipt Form')
        parm = {
            'ids': "where payment.id in ({0})".format(", ".join([str(i) for i in ids])),
            'iscopy': "%s" % self.env.context.get('iscopy', 0),
            'p_language': self.p_language,
            'p_locale': 'th' if self.date_type == 'BE' else 'en',
            'p_DateFormat': str(self.date_format),
            'p_company_en': "THE AUTO-INFO CO.,LTD.",
            'p_company_th': "บริษัท ออโต้อินโฟ จำกัด",
            'p_com_address_en': "1359 Soi Ladprao 94 (Panjamitr) Ladprao Rd.,Plubpla, Wangthonglang Bangkok 10310, Thailand.",
            'p_com_address_th': "1359 ซ.ลาดพร้าว 94 (ปัญจมิตร) ถ.ลาดพร้าว แขวงพลับพลา เขตวังทองหลาง กรุงเทพฯ 10310",
            'p_com_website': "www.auto-info.co.th",
            'p_remark': """<br>- โปรดสั่งจ่ายเช็คขีดคร่อมในนาม บริษัท ออโต้อินโฟ จำกัด <br>- กรุณาโอนเงินเข้าบัญชีธนาคารกสิกรไทย สาขาศรีวรา ทาว์อินทาวน์ เลขที่บัญชี 609-2-00057-3 (ออมทรัพย์)<br>- เมื่อพ้นกำหนดชำระเงินแล้ว บริษัทฯ จะคิดดอกเบี้ยในอัตราร้อยละ 1.5% ต่อเดือน<br>- สินค้าตามรายการข้างต้นยังเป็นสิทธิ์ของบริษัท ออโต้อินโฟ จำกัด จนกว่าผู้ซื้อจะชำระสินค้าครบเรียบร้อยแล้ว"""

        }

        return parm