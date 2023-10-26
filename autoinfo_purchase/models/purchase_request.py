from odoo import fields, models, api, _


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    job_no = fields.Char(string='Job No.', related='project_id.job_no')
    project_analytic_account_id = fields.Many2one('account.analytic.account', string='Project Analytic Account', related='project_id.analytic_account_id')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New') and 'department_id' in vals:
            department_id = self.env['hr.department'].browse(int(vals['department_id']))
            if department_id and department_id.pr_sequence_id:
                vals['name'] = department_id.pr_sequence_id.next_by_id(sequence_date=vals.get('date_start')) or '/'
        return super(PurchaseRequest, self).create(vals)

    @api.model
    def _get_default_name(self):
        if self.department_id and self.date_start:
            return self.department_id.pr_sequence_id.next_by_id(sequence_date=self.date_start) or '/'
        return self.env["ir.sequence"].next_by_code("purchase.request")

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    attention_id = fields.Many2one('res.users', string='Attention', tracking=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=False, states=READONLY_STATES, change_default=True, tracking=True, 
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    your_ref = fields.Char(string='Your Ref.')

    amount_untaxed_before_discount = fields.Float(string='Untaxed Amount before Discount', store=True, compute="_amount_all", readonly=True, digits='Discount')
    amount_discount = fields.Monetary(string='Discount Amount', store=True, compute="_amount_all", readonly=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    @api.depends('line_ids.price_total')
    def _amount_all(self):
        for request in self:
            amount_untaxed = amount_tax = amount_untaxed_before_discount = 0.0
            for line in request.line_ids.filtered(lambda line: not line.display_type):
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_untaxed_before_discount += line.price_subtotal if not line.is_trade_discount else 0.0
            currency = request.currency_id or request.partner_id.property_purchase_currency_id or self.env.company.currency_id
            request.update({
                'amount_untaxed': currency.round(amount_untaxed),
                'amount_tax': currency.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
                'amount_untaxed_before_discount': amount_untaxed_before_discount,
                'amount_discount': amount_untaxed_before_discount - amount_untaxed,
            })

    trade_discount = fields.Float(string='Trade Discount', store=True)
    trade_discount_type = fields.Selection([
        ('percent', '%'),
        ('amount', 'Amount'),
    ], string='Discount Type', default='percent')


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    partner_id = fields.Many2one('res.partner', related='request_id.partner_id', string='Partner', readonly=True, store=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    discount = fields.Float(string='Discount', digits='Discount', default=0.0, help='Discount in Order Line')
    discount_type = fields.Selection([
        ('percent', '%'),
        ('amount', 'Amount'),
        ('amount_per_unit', 'Amount (per unit)'),
    ], string='Discount Type', default='percent')
    taxes_id = fields.Many2many('account.tax', 'purchase_request_line_tax_rel', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    @api.depends('product_qty', 'product_uom_id', 'price_unit', 'discount', 'discount_type', 'taxes_id')
    def _compute_amount(self):
        for line in self:

            new_price_unit = 0
            price_unit_for_calculate_tax = 0
            product_qty = line.product_qty

            if line.discount_type == 'percent':
                new_price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                price_unit_for_calculate_tax = new_price_unit

            elif line.discount_type == 'amount':
                price = (line.price_unit * line.product_qty) - line.discount
                new_price_unit = price
                product_qty = 1
                price_unit_for_calculate_tax = new_price_unit

            elif line.discount_type == 'amount_per_unit':
                new_price_unit = line.price_unit - line.discount
                price_unit_for_calculate_tax = new_price_unit

            else:
                new_price_unit = line.price_unit
                price_unit_for_calculate_tax = new_price_unit

            tax = line.taxes_id.compute_all(price_unit_for_calculate_tax, line.request_id.currency_id, product_qty, product=line.product_id, partner=line.request_id.partner_id)
            taxes = line.taxes_id.compute_all(new_price_unit, line.request_id.currency_id, product_qty, product=line.product_id, partner=line.request_id.partner_id)
            
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in tax.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    is_trade_discount = fields.Boolean('Is Trade Discount?', default=False)
