# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.
import os
import base64
import pyscreenshot as ImageGrab
from PIL import ImageGrab
from odoo import models

# the list of models data which are to be skipped in the deleted records list.
SKIPPEDTABLELIST = [
    "deleted.records",
    "ir.attachment",
    "mail.followers",
    "mail.message",
    "mail.mail",
    "ir.model.data",
    "bus.bus",
]


class BaseModelExtend(models.AbstractModel):
    """
    Base Model Extended.
    """

    _inherit = "base"

    def unlink(self):
        """
        @ovveride:To store the deleted record
        """
        if self and not self._transient and self._name not in SKIPPEDTABLELIST:
            """ It will take screenshot if any user delete any records.
            So admin user can view deleted records data."""
            screenshot = ImageGrab.grab()
            screenshot.save("/tmp/screenshot.png")
            model_name = self._name
            # Fetch models id of deleted record.
            model_rec = self.env["ir.model"].sudo().search([("model", "=", model_name)])
            for rec in self:
                # Created deleted history record.
                deleted_rec = (
                    self.env["deleted.records"]
                    .sudo()
                    .create(
                        {
                            "name": rec.get_display_name(),
                            "model_id": model_rec.id,
                            "user_id": self.env.user.id,
                        }
                    )
                )
                with open("/tmp/screenshot.png", "rb") as img:
                    encode_image = base64.b64encode(img.read())
                # Created attechment for deleted rec which stores screenshot.
                self.env["ir.attachment"].create(
                    {
                        "res_model": "deleted.records",
                        "res_id": deleted_rec.id,
                        "datas": encode_image,
                        "type": "binary",
                        "name": rec.get_display_name(),
                    }
                )

            # Removed screenshot from system after saving in attachment.
            os.remove("/tmp/screenshot.png")

        return super(BaseModelExtend, self).unlink()

    def get_display_name(self):
        """Get display name of deleted records to write in
          deleted_records models."""
        name = False
        if self._fields.get("name") and self.name:
            name = self.name + ", " + str(self.id)
        if not name and self._fields.get("display_name") and self.display_name:
            name = self.display_name + ", " + str(self.id)
        if not name and self._rec_name:
            sql_query = """SELECT %s from %s where id = %s"""
            params = (self._rec_name, self._table, self.id)
            self.env.cr.execute(sql_query, params)
            results = self.env.cr.dictfetchall()
            name = results[0].get(self._rec_name)
            name += ", " + str(self.id)

        return name
