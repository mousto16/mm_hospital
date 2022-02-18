# -*- coding : utf-8 -*-

from odoo import api, fields, models, _

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    date_appointment = fields.Date(string='Date', required=False)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)


    """create record"""
    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        """Pour appeler la view appointment"""
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'target': 'new'
        }


    def action_view_appointment(self):
        #method 1
        action = self.env.ref('mm_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

        # method 2
        #action = self.env["ir.actions.actions"]._for_xml_id("mm_hospital.action_hospital_appointment"
        #action['domain'] = [('patient_id', '=', self.patient_id.id)]
        #return action

        # method 3
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Appointments',
        #     'res_model': 'hospital.appointment',
        #     'view_type': 'form',
        #     'domain': [('patient_id', '=', self.patient_id.id)],
        #     'view_mode': 'tree,kanban,form',
        #     #'views': [(False, "form")],
        #     'target': 'current'
        # }

