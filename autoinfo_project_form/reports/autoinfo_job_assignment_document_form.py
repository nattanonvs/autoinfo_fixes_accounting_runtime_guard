# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api
from odoo.tools import config
from odoo.exceptions import ValidationError


class AutoinfoJobAssignmentDocumentForm(models.TransientModel):
    _name = 'autoinfo.job.assignment.document.form'
    _description = 'autoinfo.job.assignment.document.form'
    _inherit = 'dtr.jasper.report'

    def _compute_default_date_type(self):
        rpt = self.env.ref('autoinfo_project_form.autoinfo_job_assignment_document_form_code')
        return rpt.date_type

    def _compute_default_date_format(self):
        rpt = self.env.ref('autoinfo_project_form.autoinfo_job_assignment_document_form_code')
        return rpt.date_format

    name = fields.Char()
    jasper_file = fields.Char(default=lambda self: self.get_jasper_file(__file__))
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

    def show_report(self, report_name=False):
        ids = self.env.context.get('active_ids')
        rpt = self.env.ref('autoinfo_project_form.autoinfo_job_assignment_document_form_code')
        if rpt and not rpt.allow:
            self.err_msg = 'Unallow Report'
            raise ValidationError('Unallow Report')

        email_subject = 'Job Assignment Document'
        email_document_number = ''
        if len(ids) == 1:
            data = self.env['project.project'].search([('id', '=', ids)], limit=1)
            email_subject = 'Job Assignment Document: ' + data.name
            email_document_number = data.name
            self.can_send_email = True

        return super(AutoinfoJobAssignmentDocumentForm, self).show_report(email_subject=email_subject, email_document_number=email_document_number)

    def get_parameters(self):
        ids = self.env.context.get('active_ids')
        p_where = "WHERE pro.id in ({0})".format(", ".join([str(i) for i in ids]))
        rpt = self.env.ref('autoinfo_project_form.autoinfo_job_assignment_document_form_code')
        iso_no = rpt.iso_no or ""
        path = "{0}/filestore/{1}/".format(config.options['data_dir'].replace('\\', '/'), self.env.cr.dbname)

        self.name = self.get_file_name(ids, 'project.project', 'Job Assignment Document Form')
        return {
            'p_Where': p_where,
            'p_ISO': iso_no,
            'p_DateFormat': str(self.date_format),
            'p_language': self.p_language,
            'p_locale': 'th' if self.date_type == 'BE' else 'en',
            'p_Printby': self.env.user.name,
            'p_Path': path
        }
