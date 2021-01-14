# -*- coding: utf-8 -*-

{
    'name': 'Airline',
    'sequence': 1222,
    'version': '1.0',
    'depends': ['mail','base','product','sale'],
    'category': 'sale','crm'
    'summary': 'Handle lunch orders of your employees',
    'description': """
The base module to manage lunch.
================================
Cost sheet from CRM, Generate Quotation
    """,
    'data': [
        'views/view.xml',
        # 'wizard/report_wizard.xml',
        # 'views/ticket_report2.xml',
        'views/ticket_report.xml',
        'views/ticket_report_template.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': True,
}
