from odoo import fields, models, api
from odoo.exceptions import ValidationError

from odoo.tools import config

class autoinfo_receipt_pp_form(models.TransientModel):
    _name = 'autoinfo.receipt.pp.form'
    _description = 'Autoinfo Receipt Preprint Form'
    _inherit = 'dtr.jasper.report'

    def _compute_default_date_type(self):
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        return rpt.date_type

    def _compute_default_date_format(self):
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        return rpt.date_format

    name = fields.Char('Autoinfo Receipt Preprint Form')

    jasper_file = fields.Char(default=lambda self: self.get_jasper_file(__file__))
    p_language = fields.Selection([
        ('thai', u'Thai'),
        ('english', u'English')], 'Document Language', default='thai')

    date_type = fields.Selection([('AD', 'AD'), ('BE', 'BE')], 'Date Type', default=_compute_default_date_type,
                                 help='AD = คริสตศักราช\nBE = พุทธศักราช')
    date_format = fields.Selection([('dd-MM-yy', 'dd-MM-yy'),
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

    def show_report(self, report_name=False):
        ids = self.env.context.get('active_ids')

        email_subject = 'Customer Receipt Form'
        email_document_number = ''
        if len(ids) == 1:
            data = self.env['account.payment'].search([('id', '=', ids)], limit=1)
            email_subject = 'Customer Receipt Form: ' + data.name
            email_document_number = data.name
            self.can_send_email = True

        return super(autoinfo_receipt_pp_form, self).show_report(email_subject=email_subject,
                                                    email_document_number=email_document_number)

    def get_parameters(self):
        ids = self.env.context.get('active_ids')
        recv = "WHERE pay.id in ({0})".format(", ".join([str(i) for i in ids]))

        rpt = self.env.ref('dtr_accounting_form.f_ac_007')
        if rpt and not rpt.allow:
            self.err_msg = 'Unallow Report'
            raise ValidationError('Unallow Report')

        iso_no = rpt.iso_no or ""
        path = "{0}/filestore/{1}/".format(config.options['data_dir'].replace('\\', '/'), self.env.cr.dbname)

        # self.name = 'Receipt Report'
        self.name = self.get_file_name(ids, 'account.payment', 'Receipt Report')
        return {
            'ids': recv,
            'p_language': str(self.p_language),
            'p_DateFormat': str(self.date_format),
            'p_locale': 'th' if self.date_type == 'BE' else 'en'
        }
