# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor "
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _rec_name = "doctor_name" #faire reference au champ doctor_name

    doctor_name = fields.Char(string='Name', required=True, tracking=True)

    age = fields.Integer(string='Age', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', copy=False)

    image = fields.Binary(string='Doctor Image')

    # le champ active pour l'archivage
    active = fields.Boolean(string="Active", default=True)

    appointment_count = fields.Integer(string='Apppointment Count', compute = '_compute_appointment_count')

    def _compute_appointment_count(self):
        """singleton Error : using loop for"""
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=',rec.id)])
            rec.appointment_count = appointment_count

    # pour gerer la copie lors de la duplication
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (Copy)") % (self.doctor_name)
        return super(HospitalDoctor, self).copy(default=default)
