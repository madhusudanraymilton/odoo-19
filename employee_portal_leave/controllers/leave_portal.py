from odoo import http
from odoo.http import request
from datetime import datetime
import base64


class PortalLeaveController(http.Controller):

    @http.route('/my/leave/apply', type='http', auth='user', website=True)
    def apply_leave(self, **kw):
        """Render leave application form"""
        try:
            # Get current user's employee record
            employee = request.env['hr.employee'].search([
                ('user_id', '=', request.env.user.id)
            ], limit=1)

            if not employee:
                return request.render('employee_portal_leave.portal_no_employee', {
                    'error': 'No employee record found for your account. Please contact HR.'
                })

            # Get active leave types with allocation check
            leave_types = request.env['hr.leave.type'].search([
                ('active', '=', True),
                ('requires_allocation', '=', 'no')  # Or check allocations
            ])

            # Get employees for delegation (active employees excluding current user)
            employees = request.env['hr.employee'].search([
                ('id', '!=', employee.id),
                ('active', '=', True)
            ], order='name')

            # Get leave allocations for display
            allocations = request.env['hr.leave.allocation'].search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'validate')
            ])

            return request.render('employee_portal_leave.portal_apply_leave', {
                'leave_types': leave_types,
                'employees': employees,
                'allocations': allocations,
                'employee': employee,
                'csrf': request.csrf_token(),
                'error': kw.get('error'),
                'success': kw.get('success'),
            })

        except Exception as e:
            return request.render('employee_portal_leave.portal_error', {
                'error': str(e)
            })

    @http.route('/my/leave/submit', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def submit_leave(self, **post):
        """Handle leave submission with validation"""
        try:
            user = request.env.user

            # Get employee linked to portal user
            employee = request.env['hr.employee'].search([
                ('user_id', '=', user.id)
            ], limit=1)

            if not employee:
                return request.redirect('/my/leave/apply?error=No employee record found')

            # Validate dates
            date_from = post.get('date_from')
            date_to = post.get('date_to')
            
            if not date_from or not date_to:
                return request.redirect('/my/leave/apply?error=Please provide both start and end dates')

            # Convert to date objects for validation
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            except ValueError:
                return request.redirect('/my/leave/apply?error=Invalid date format')

            # Check if date_from is before date_to
            if date_from_obj > date_to_obj:
                return request.redirect('/my/leave/apply?error=Start date cannot be after end date')

            # Check if dates are in the past
            today = datetime.now().date()
            if date_from_obj < today:
                return request.redirect('/my/leave/apply?error=Cannot apply for past dates')

            # Validate leave type
            leave_type_id = post.get('leave_type')
            if not leave_type_id:
                return request.redirect('/my/leave/apply?error=Please select a leave type')

            leave_type = request.env['hr.leave.type'].browse(int(leave_type_id))
            if not leave_type.exists():
                return request.redirect('/my/leave/apply?error=Invalid leave type')

            # Check for overlapping leaves
            overlapping = request.env['hr.leave'].search([
                ('employee_id', '=', employee.id),
                ('state', 'not in', ['refuse', 'cancel']),
                ('request_date_from', '<=', date_to),
                ('request_date_to', '>=', date_from),
            ])

            if overlapping:
                return request.redirect('/my/leave/apply?error=You already have a leave request for these dates')

            # Build leave values
            vals = {
                'employee_id': employee.id,
                'holiday_status_id': int(leave_type_id),
                'request_date_from': date_from,
                'request_date_to': date_to,
                'name': post.get('reason', 'Leave Request').strip() or 'Leave Request',
            }

            # Add delegation if provided
            delegate_id = post.get('delegate_employee_id')
            if delegate_id and delegate_id.strip():
                vals['delegate_employee_id'] = int(delegate_id)

            # Create leave request
            leave = request.env['hr.leave'].sudo().create(vals)

            if not leave:
                return request.redirect('/my/leave/apply?error=Failed to create leave request')

            # Handle file attachment
            if 'attachment' in request.httprequest.files:
                attachment_file = request.httprequest.files['attachment']
                if attachment_file and attachment_file.filename:
                    # Validate file size (max 5MB)
                    attachment_file.seek(0, 2)  # Seek to end
                    file_size = attachment_file.tell()
                    attachment_file.seek(0)  # Reset to beginning
                    
                    if file_size > 5 * 1024 * 1024:  # 5MB
                        leave.sudo().unlink()
                        return request.redirect('/my/leave/apply?error=File size exceeds 5MB limit')

                    # Validate file type
                    allowed_extensions = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
                    file_ext = attachment_file.filename.split('.')[-1].lower()
                    
                    if file_ext not in allowed_extensions:
                        leave.sudo().unlink()
                        return request.redirect('/my/leave/apply?error=Invalid file type')

                    attachment_data = base64.b64encode(attachment_file.read())
                    request.env['ir.attachment'].sudo().create({
                        'name': attachment_file.filename,
                        'type': 'binary',
                        'datas': attachment_data,
                        'res_model': 'hr.leave',
                        'res_id': leave.id,
                        'mimetype': attachment_file.content_type,
                    })

            return request.redirect('/my/leave/history?success=Leave request submitted successfully')

        except ValueError as e:
            return request.redirect(f'/my/leave/apply?error=Invalid input: {str(e)}')
        except Exception as e:
            return request.redirect(f'/my/leave/apply?error=An error occurred: {str(e)}')

    @http.route('/my/leave/history', type='http', auth='user', website=True)
    def leave_history(self, **kw):
        """Display leave history with filters"""
        try:
            user = request.env.user
            
            # Get employee
            employee = request.env['hr.employee'].search([
                ('user_id', '=', user.id)
            ], limit=1)

            if not employee:
                return request.render('employee_portal_leave.portal_no_employee', {
                    'error': 'No employee record found'
                })

            # Build domain for search
            domain = [('employee_id', '=', employee.id)]
            
            # Filter by status if provided
            status_filter = kw.get('status')
            if status_filter:
                domain.append(('state', '=', status_filter))

            # Get leaves
            leaves = request.env['hr.leave'].search(
                domain,
                order='request_date_from desc'
            )

            # Get leave statistics
            stats = {
                'total': len(leaves),
                'pending': len(leaves.filtered(lambda l: l.state == 'confirm')),
                'approved': len(leaves.filtered(lambda l: l.state == 'validate')),
                'refused': len(leaves.filtered(lambda l: l.state == 'refuse')),
            }

            return request.render('employee_portal_leave.portal_leave_history', {
                'leaves': leaves,
                'stats': stats,
                'status_filter': status_filter,
                'success': kw.get('success'),
            })

        except Exception as e:
            return request.render('employee_portal_leave.portal_error', {
                'error': str(e)
            })

    @http.route('/my/leave/cancel/<int:leave_id>', type='http', auth='user', website=True, csrf=True)
    def cancel_leave(self, leave_id, **kw):
        """Cancel a pending leave request"""
        try:
            leave = request.env['hr.leave'].browse(leave_id)
            
            # Check if leave exists and belongs to current user
            if not leave.exists() or leave.employee_id.user_id.id != request.env.user.id:
                return request.redirect('/my/leave/history?error=Leave request not found')

            # Only allow cancellation of draft or pending requests
            if leave.state not in ['draft', 'confirm']:
                return request.redirect('/my/leave/history?error=Cannot cancel this leave request')

            leave.sudo().action_refuse()
            
            return request.redirect('/my/leave/history?success=Leave request cancelled successfully')

        except Exception as e:
            return request.redirect(f'/my/leave/history?error=Error cancelling leave: {str(e)}')

    @http.route('/my/leave/balance', type='json', auth='user')
    def get_leave_balance(self, leave_type_id):
        """Get remaining leave balance for a specific leave type"""
        try:
            employee = request.env['hr.employee'].search([
                ('user_id', '=', request.env.user.id)
            ], limit=1)

            if not employee:
                return {'error': 'No employee record found'}

            allocation = request.env['hr.leave.allocation'].search([
                ('employee_id', '=', employee.id),
                ('holiday_status_id', '=', int(leave_type_id)),
                ('state', '=', 'validate')
            ], limit=1)

            if allocation:
                return {
                    'balance': allocation.number_of_days,
                    'used': allocation.leaves_taken,
                    'remaining': allocation.number_of_days - allocation.leaves_taken
                }
            
            return {'balance': 0, 'used': 0, 'remaining': 0}

        except Exception as e:
            return {'error': str(e)}