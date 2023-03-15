# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os


class PrepaymentForm(models.TransientModel):
    _inherit = 'prepayment.form'

    def show_report(self):
        path = os.path.split(os.path.abspath(__file__))[0]
        file_name = "autoinfo_prepayment_form.jasper"
        self.jasper_file = os.path.join(os.path.dirname(path), 'jrxml', file_name)
        return super(PrepaymentForm, self).show_report()
