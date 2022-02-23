# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'summary': "Hospital Management Mousto",
    'version': '1.0',
    'depends': [
        'sale',
        'mail',
        'website_slides',
        'hr',
        'report_xlsx'
    ],
    'author': "Moustapha",
    'category': 'Productivity',
    'description': """
    This module is management of Hospital
    """,
    'sequence':-100,
    'website': 'camersoftware.com',
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',
        'views/patient.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/sale.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'report/patient_details_template.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 104,
    'currency': 'EUR'
}
