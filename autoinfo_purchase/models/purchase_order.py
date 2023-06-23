from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New' and 'department_id' in vals:
            department_id = self.env['hr.department'].browse(int(vals['department_id']))
            if department_id and department_id.po_sequence_id:
                seq_date = None
                if 'date_order' in vals:
                    seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
                vals['name'] = department_id.po_sequence_id.next_by_id(sequence_date=seq_date) or '/'
        return super(PurchaseOrder, self).create(vals)

    attention_id = fields.Many2one('res.users', string='Attention', tracking=True, index=True)
