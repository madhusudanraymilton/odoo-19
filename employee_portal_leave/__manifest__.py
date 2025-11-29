{
    'name': 'Employee Portal Leave Management',
    'version': '1.0',
    'category': 'Portal',
    'depends': ['website', 'portal', 'hr_holidays'],
    'data': [
        'security/portal_leave_security.xml',
        'security/ir.model.access.csv',
        'views/portal_apply_leave.xml',
        'views/portal_leave_history.xml',
    ],
    'installable': True,
}
