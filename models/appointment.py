# -*- coding : utf-8 -*-

from odoo import api, fields, models, _

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment "
    _inherit = ["mail.thread", 'mail.activity.mixin']

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string='Date')
    date_checkup = fields.Datetime(string='Check Up Time')
    """add to header in form view"""
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default ='draft',
                             string='Status', tracking=True)

    """add create dynamic field (many2one), define Many2one field"""
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)

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
    programme add new message New Appointment"""
    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = 'New Appointment'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res