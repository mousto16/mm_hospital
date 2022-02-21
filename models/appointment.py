# -*- coding : utf-8 -*-

from odoo import api, fields, models, _

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment "
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _order = "name desc" #classement par ordre decroissant

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))

    """add create dynamic field (many2one), define Many2one field"""
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)


    """related field init (faire apparaitre l'age de chaque patient quant on le selectionne dans appointment) """
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True)

    """related field (faire apparaitre le esxe de chaque patient quant on le selectionne dans appointment avec onchange) """
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")

    """add to header in form view"""
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string='Status', tracking=True)

    note = fields.Text(string='Description')
    date_appointment = fields.Date(string='Date')
    date_checkup = fields.Datetime(string='Check Up Time')
    prescription = fields.Text(String="Prescription") #dans le notebook


    """define fonction to change the steps to the statusbar of header of view form"""
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

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

    """For field of string"""
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''
