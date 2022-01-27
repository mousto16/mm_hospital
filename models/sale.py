# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    """Inherit for use the table existing in the database"""
    _inherit = "sale.order"

    sale_description = fields.Char(string='Sale Description')
