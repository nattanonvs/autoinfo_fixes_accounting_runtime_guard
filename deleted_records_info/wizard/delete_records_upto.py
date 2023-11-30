# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.
from odoo import fields, models


class DeleteRecordsUpto(models.TransientModel):
    """Class for movein moveout information."""

    _name = "delete.records.upto"
    _description = "This model will delete the deleted records within given date"

    date = fields.Date(string="Date", default=fields.Date.context_today)

    def delete_records_upto_date(self):
        """Method call for deleting records."""
        self.env["deleted.records"].search([("create_date", "<", self.date)]).unlink()
