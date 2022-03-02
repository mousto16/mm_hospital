#-*-coding:utf-8

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class HospitalController(http.Controller):
    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):

        doctor_rec = request.env['hospital.doctor'].sudo().search([])
        return http.request.render('mm_hospital.create_patient', {'patient_name':'Camer Software',
                                                                  'doctor_rec': doctor_rec})

    @http.route('/create/webpatient', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        request.env['hospital.patient'].sudo().create(kw)
        return http.request.render('mm_hospital.patient_thanks', {})
        # doctor_val = {
        #     'doctor_id' : kw.get('doctor_id')
        # }
        # request.env['hospital.doctor'].sudo().create(doctor_val)
