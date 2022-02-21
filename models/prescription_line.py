# -*- coding : utf-8 -*-

from odoo import api, fields, models, _

class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medecine")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

