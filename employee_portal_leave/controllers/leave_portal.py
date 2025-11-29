"""
from odoo import http
from odoo.http import request

class PortalLeaveController(http.Controller):

    @http.route('/my/leave/apply', type='http', auth='user', website=True)
    def apply_leave(self, **kw):
        leave_types = request.env['hr.leave.type'].sudo().search([])
        return request.render('employee_portal_leave.portal_apply_leave', {
            'leave_types': leave_types,
            'csrf': request.csrf_token(),
        })

    @http.route('/my/leave/submit', type='http', auth='user', website=True, methods=['POST'])
    def submit_leave(self, **post):
        user = request.env.user

        # Get employee linked to portal user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        if not employee:
            return request.redirect('/my/leave/apply')

        # Build values
        vals = {
            'employee_id': employee.id,
            'holiday_status_id': int(post.get('leave_type')),
            'request_date_from': post.get('date_from'),
            'request_date_to': post.get('date_to'),
            'name': post.get('reason'),
        }

        # Create leave with sudo
        leave = request.env['hr.leave'].sudo().create(vals)

        # If failed → reload form
        if not leave:
            return request.redirect('/my/leave/apply')

        # Success → redirect to history
        return request.redirect('/my/leave/history')

    @http.route('/my/leave/history', type='http', auth='user', website=True)
    def leave_history(self, **kw):
        user = request.env.user
        leaves = request.env['hr.leave'].sudo().search([
            ('employee_id.user_id', '=', user.id)
        ])

        return request.render('employee_portal_leave.portal_leave_history', {
            'leaves': leaves,
        })

"""
from odoo import http
from odoo.http import request
import base64


class PortalLeaveController(http.Controller):

    @http.route('/my/leave/apply', type='http', auth='user', website=True)
    def apply_leave(self, **kw):
        # Get only active leave types that are available for portal
        leave_types = request.env['hr.leave.type'].sudo().search([
            ('active', '=', True),
            # Add any additional filters for portal availability if needed
        ])

        # Get employees for delegation (excluding current user's employee)
        user_employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

        employees = request.env['hr.employee'].sudo().search([
            ('id', '!=', user_employee.id),
            ('active', '=', True)
        ])

        return request.render('employee_portal_leave.portal_apply_leave', {
            'leave_types': leave_types,
            'employees': employees,
            'csrf': request.csrf_token(),
        })

    @http.route('/my/leave/submit', type='http', auth='user', website=True, methods=['POST'])
    def submit_leave(self, **post):
        user = request.env.user

        # Get employee linked to portal user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        if not employee:
            return request.redirect('/my/leave/apply')

        # Build values
        vals = {
            'employee_id': employee.id,
            'holiday_status_id': int(post.get('leave_type')),
            'request_date_from': post.get('date_from'),
            'request_date_to': post.get('date_to'),
            'name': post.get('reason'),
        }

        # Add delegation fields if provided
        if post.get('delegate_employee_id'):
            vals['delegate_employee_id'] = int(post.get('delegate_employee_id'))

        if post.get('batch_id'):
            vals['batch_id'] = post.get('batch_id')

        # Create leave with sudo
        leave = request.env['hr.leave'].sudo().create(vals)

        # Handle attachment if provided
        if 'attachment' in request.httprequest.files:
            attachment_file = request.httprequest.files['attachment']
            if attachment_file and attachment_file.filename:
                attachment_data = base64.b64encode(attachment_file.read())
                request.env['ir.attachment'].sudo().create({
                    'name': attachment_file.filename,
                    'type': 'binary',
                    'datas': attachment_data,
                    'res_model': 'hr.leave',
                    'res_id': leave.id,
                    'mimetype': attachment_file.content_type,
                })

        # If failed → reload form
        if not leave:
            return request.redirect('/my/leave/apply')

        # Success → redirect to history
        return request.redirect('/my/leave/history')

    @http.route('/my/leave/history', type='http', auth='user', website=True)
    def leave_history(self, **kw):
        user = request.env.user
        leaves = request.env['hr.leave'].sudo().search([
            ('employee_id.user_id', '=', user.id)
        ])

        return request.render('employee_portal_leave.portal_leave_history', {
            'leaves': leaves,
        })