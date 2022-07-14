from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    scheduled_date = fields.Datetime(string='Scheduled Date', compute='_compute_scheduled_date', store=True)
    is_all_delivered = fields.Boolean(string='Is Delivered?', compute='_compute_is_all_delivered', store=True)
    commitment_date = fields.Datetime('Delivery Date', copy=False,states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
      help="This is the delivery date promised to the customer. "
           "If set, the delivery order will be scheduled based on "
           "this date rather than product lead times.", track_visibility='onchange')
    reason_change_delivery_date = fields.Text(string='Reason Change Delivery Date', copy=False)

    @api.depends('picking_ids.scheduled_date')
    def _compute_scheduled_date(self):
        for rec in self:
            picking_ids = rec.picking_ids.filtered(lambda x: x.scheduled_date and x.state not in ['cancel'])
            if picking_ids:
                rec.scheduled_date = max(picking_ids.mapped('scheduled_date'))
            else:
                rec.scheduled_date = False

    @api.depends('picking_ids.state')
    def _compute_is_all_delivered(self):
        for rec in self:
            if any(picking_id.state not in ['done', 'delivered', 'cancel'] for picking_id in rec.picking_ids):
                rec.is_all_delivered = False
            else:
                rec.is_all_delivered = True

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New') and vals.get('user_id'):
            sale_person = self.env['res.users'].sudo().browse(vals.get('user_id'))
            if sale_person.quotation_sequence_id:
                vals['name'] = sale_person.quotation_sequence_id.next_by_id(sequence_date=vals.get('date_order'))
        return super(SaleOrder, self).create(vals)
