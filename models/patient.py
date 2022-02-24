# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient "
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _order = "id desc" #classement par ordre decroissant

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
    image = fields.Binary(string='Patient Image')

    appointment_ids = fields.One2many('hospital.appointment', 'patient_id',
                                            string='Appointments')

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

    """function define the default value (New, description, gender:male, age...)"""
    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        res['gender'] = 'female'
        res['age'] = 18
        return res

    """Pour gerer les contrainte dans la base de donnee: si un patient est deja cree, on ne devrait plus creer ce meme patient"""
    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name','=', rec.name), ('id','!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    """ Si l'age vaut 0, l'enregistrement au niveau de la base de donnee"""
    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age ==0:
                raise ValidationError(_("Age Cannot Be Zero..."))

    """Combiner la plusieurs champs lors de la selection dans le Many2one (reference et name patient)"""
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + ']' + ' ' + rec.name
            result.append((rec.id, name))
        return result

    """Pour gerer les boutons au dessus des informations dans une affichage du patient"""
    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            # 'view_type': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree,kanban,form',
            # 'views': [(False, "form")],
            'target': 'current'
        }
