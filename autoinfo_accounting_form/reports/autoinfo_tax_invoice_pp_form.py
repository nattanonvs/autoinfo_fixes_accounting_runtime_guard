from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import config


class autoinfo_tax_invoice_pp_form(models.TransientModel):
    _name = 'autoinfo.tax.invoice.pp.form'
    _description = 'Autoinfo Tax Invoice Preprint Form'
    _inherit = 'dtr.jasper.report'

    def _compute_default_date_type(self):
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        return rpt.date_type

    def _compute_default_date_format(self):
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        return rpt.date_format

    name = fields.Char('Autoinfo Tax Invoice Preprint Form')

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
    show_inv_name = fields.Boolean(string='Show Invoice Name', default=False)

    def show_report(self, report_name=False):
        ids = self.env.context.get('active_ids')

        email_subject = 'Customer Invoices Form (Autoinfo)'
        email_document_number = ''
        if len(ids) == 1:
            data = self.env['account.move'].search([('id', 'in', ids)], limit=1)
            email_subject = 'Customer Invoices Form: ' + data.name
            email_document_number = data.name
            self.can_send_email = True

        # Running Line Sequence before Show Report
        for order in self.env['account.move'].search([('id', 'in', ids)]):
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
        return super(autoinfo_tax_invoice_pp_form, self).show_report(email_subject=email_subject,
                                                    email_document_number=email_document_number)

    def get_parameters(self):
        ids = self.env.context.get('active_ids')
        acc_moves = self.env['account.move'].browse(ids)
        if acc_moves.filtered(lambda x: x.move_type not in ['in_invoice', 'out_invoice'] or x.dncn in ['dn', 'cn']):
            self.err_msg = 'Cannot print document is not customer invoices or vendor bills'
            raise ValidationError('Cannot print document is not customer invoices or vendor bills')
        rpt = self.env.ref('dtr_accounting_form.f_ac_001')
        if rpt and not rpt.allow:
            self.err_msg = "Unallow Report"
            raise ValidationError("Unallow Report")
        # self.name = 'Invoice Report'
        self.name = self.get_file_name(ids, 'account.move', 'Invoice Report')
        parm = {
            'ids': "where invoice.id in ({0})".format(", ".join([str(i) for i in ids])),
            'iscopy': "%s" % self.env.context.get('iscopy', 0),
            'p_language': self.p_language,
            'p_locale': 'th' if self.date_type == 'BE' else 'en',
            'p_DateFormat': str(self.date_format),
            'p_Path': "{0}/filestore/{1}/".format(config.options['data_dir'].replace('\\', '/'), self.env.cr.dbname),
            'show_inv_name': str(self.show_inv_name)
        }
        return parm


