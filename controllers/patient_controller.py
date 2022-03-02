#-*-coding:utf-8

from odoo import http
from odoo.http import request
#from odoo.addons.website_sale.controllers.main import WebsiteSale

class PatientController(http.Controller):

    @http.route('/hospital/patient/', auth='public', website=True)
    def hospital_patient(self, **kw):
        # return "Thanks for watching"
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render('mm_hospital.patients_page', {
            'patients':patients
        })

