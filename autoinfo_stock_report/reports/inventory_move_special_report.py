# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools import config
import os


class InventoryMoveSpecialReport(models.TransientModel):
    _inherit = 'inventory.move.special.report'

    p_department_id = fields.Many2one('hr.department', string='Department')

    def get_context(self):
        context = super(InventoryMoveSpecialReport, self).get_context()
        context.update({'default_p_department_id': self.p_department_id.id})
        return context

    def get_parameters(self):
        res = super(InventoryMoveSpecialReport, self).get_parameters()
        if self.p_department_id:
            child_department_ids = self.env['hr.department'].search([('parent_id', '=', self.p_department_id.id)])
            department_ids = child_department_ids + self.p_department_id
            condition = res.get('p_Where')
            condition += ' AND sp.department_id in ({0})'.format(', '.join([str(i.id) for i in department_ids]))
            res.update({'p_Where': condition})
        return res
