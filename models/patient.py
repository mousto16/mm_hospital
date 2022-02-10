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

    """Count the number of appointment by patient"""
    appointment_count = fields.Integer(string='Apppointment Count', compute = '_compute_appointment_count')

    """Methode to count the number of appointment by patient"""
    """correspond a : select count(*) from hospital.appointment where patient_id = self.id
                patient_id : reference au patient de appointment
                hospital.appointment: nom de la table de la base de donnee
                id = id du patient dans la table patient
            """
    def _compute_appointment_count(self):
        """singleton Error : using loop for"""

        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=',rec.id)])
            rec.appointment_count = appointment_count

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
    programme add new message New Patient"""
    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = 'New Patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res