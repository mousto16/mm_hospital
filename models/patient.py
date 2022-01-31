# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient "
    _inherit = ["mail.thread", 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    """id reference of patient"""
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    """add to header in form view"""
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default ='draft',
                             string='Status', tracking=True)

    """add create dynamic field (many2one), define Many2one field"""
    responsible_id = fields.Many2one('res.partner', string='Responsible')

    """define fonction to change the steps to the statusbar of header of view form"""
    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    """create id for Patient, if the field note isn't define, the 
    programme add new message New Patient"""
    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = 'New Patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res