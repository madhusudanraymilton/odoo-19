{
    'name': 'Employee Portal Leave Management',
    'version': '2.0.0',
    'category': 'Human Resources/Time Off',
    'summary': 'Allow portal users to apply for leaves and view leave history',
    'description': """
        Employee Portal Leave Management
        =================================
        This module allows portal users to:
        * Apply for time off/leaves
        * View leave balance
        * Track leave request status
        * Delegate work during leave
        * Upload supporting documents
        * Cancel pending requests
        * Filter leave history by status
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'website',
        'portal',
        'hr_holidays',  # Time Off module
    ],
    'data': [
        'security/portal_leave_security.xml',
        'security/ir.model.access.csv',
        'views/portal_apply_leave.xml',
        'views/portal_leave_history.xml',
        'views/hr_leave_views.xml',  # Add view for delegate field in backend
    ],
    'assets': {
        'web.assets_frontend': [
            # Add any custom CSS/JS files here if needed
            # 'employee_portal_leave/static/src/css/leave_portal.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}