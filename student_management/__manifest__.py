# -*- coding: utf-8 -*-

{
    "name": "Student Management",
    "version": "1.0",
    "author": "Madhusudan Ray",
    "website": "https://www.madhusudan.com",
    'depends': ['base'],
    'category': 'Education',
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/student_views.xml',
        'views/course_views.xml',
        'views/enrollment_views.xml',
    ],
    'images': ['static/description/logo.png'],
    "installable": True,
    "application": True,
}