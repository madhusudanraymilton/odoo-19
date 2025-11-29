{
    'name': 'Employee Portal Leave Management',
    'version': '1.2',
    'category': 'Human Resources/Time Off',
    'summary': 'Modern leave management portal for employees with enhanced UI',
    'description': """
        Employee Portal Leave Management
        =================================
        This module allows portal users to:
        * Apply for time off/leaves with modern interface
        * View leave balance in real-time
        * Track leave request status with visual indicators
        * Delegate work during leave
        * Upload supporting documents (max 5MB)
        * Cancel pending requests
        * Filter leave history by status
        * Responsive design for mobile/tablet/desktop

        Features:
        * Modern Bootstrap 5 design
        * Real-time form validation
        * Auto-calculation of leave duration
        * Balance checking before submission
        * File upload with validation
        * Email notifications (optional)
        * Comprehensive error handling
        * Detailed audit logging

        Technical Improvements:
        * Enhanced security with proper access rights
        * CSRF protection
        * SQL injection prevention
        * Optimized database queries
        * Client-side and server-side validation
        * Proper error handling and logging
    """,
    'author': 'BdCalling It Lt.',
    'website': 'https://www.bdcalling.com',
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
        'views/hr_leave_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'employee_portal_leave/static/src/css/leave_portal.css',
            'employee_portal_leave/static/src/js/leave_portal.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}