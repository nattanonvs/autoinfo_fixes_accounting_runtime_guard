# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    autoinfo_list_price = fields.Float(string='List Price', digits='Product Price')
