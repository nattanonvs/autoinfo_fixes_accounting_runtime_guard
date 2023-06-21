# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import config
from odoo.exceptions import ValidationError


class PoPurchaseRequestATReport(models.TransientModel):
    _name = 'po.purchase.request.at.report'
    _description = 'po.purchase.request.at.report'
    _inherit = 'dtr.jasper.report'

    def _compute_default_date_type(self):
        rpt = self.env.ref('autoinfo_purchase_form.f_p_100')
        return rpt.date_type

    def _compute_default_date_format(self):
        rpt = self.env.ref('autoinfo_purchase_form.f_p_100')
        return rpt.date_format

    name = fields.Char()
    jasper_file = fields.Char(default=lambda self: self.get_jasper_file(__file__))
    ad_be = fields.Char(default='AD')
    p_language = fields.Selection([
        ('thai', u'Thai'),
        ('english', u'English')], 'Language', default='thai')

    date_type = fields.Selection([('AD', 'AD'), ('BE', 'BE')], 'Date Type', default=_compute_default_date_type, help='AD = คริสตศักราช\nBE = พุทธศักราช')
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
        'Date Format',
        default=_compute_default_date_format)

    def show_report(self, report_name=False, email_subject=False, email_document_number=False):
        ids = self.env.context.get('active_ids')
        orders = self.env['purchase.request'].search([('id', 'in', ids), ('state', 'not in', ['approved', 'done'])])
        if orders and len(orders) > 0:
            raise ValidationError('Only Approved Purchase Request is allow.')

        rpt = self.env.ref('autoinfo_purchase_form.f_p_100')
        if rpt and not rpt.allow:
            self.err_msg = 'Unallow Report'
            raise ValidationError('Unallow Report')

        email_subject = 'Purchase Request'
        email_document_number = ''
        if len(ids) == 1:
            data = self.env['purchase.request'].search([('id', '=', ids)], limit=1)
            email_subject = 'Purchase Request: ' + data.name
            email_document_number = data.name
            self.can_send_email = True

        return super(PoPurchaseRequestATReport, self).show_report(email_subject=email_subject, email_document_number=email_document_number)

    def get_parameters(self):
        ids = self.env.context.get('active_ids')
        p_PRNo = "WHERE p.id in ({0})".format(", ".join([str(i) for i in ids]))
        rpt = self.env.ref('autoinfo_purchase_form.f_p_100')
        self.ad_be = rpt.date_type

        rpt = self.env.ref('autoinfo_purchase_form.f_p_100')
        iso_no = rpt.iso_no or ""
        path = "{0}/filestore/{1}/".format(config.options['data_dir'].replace('\\', '/'), self.env.cr.dbname)

        # self.name = 'Purchase Request Report'
        self.name = self.get_file_name(ids, 'purchase.request', 'Purchase Request Report')
        return {
            # 'p_Company_No': '{0}'.format(1),
            'p_PRNo': p_PRNo,
            'p_Path': path,
            'p_ISO': iso_no,
            'p_EName': str(rpt.e_name),
            'p_ESignature': str(rpt.e_signature),
            'p_DateFormat': str(self.date_format),
            'p_language': self.p_language,
            'p_locale': 'th' if self.date_type == 'BE' else 'en'
        }
