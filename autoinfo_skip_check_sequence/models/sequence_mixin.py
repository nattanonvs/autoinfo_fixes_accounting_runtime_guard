from odoo import fields, models, api


class SequenceMixin(models.AbstractModel):
    _inherit = 'sequence.mixin'

    @api.constrains(lambda self: (self._sequence_field, self._sequence_date_field))
    def _constrains_date_sequence(self):
        return
