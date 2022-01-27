# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'summary': "Hospital Management Mousto",
    'version': '1.0',
    'depends': ['sale'],
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
        'views/patient.xml',
        'views/sale.xml'
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
