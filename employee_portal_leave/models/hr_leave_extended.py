from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrLeaveExtended(models.Model):
    _inherit = 'hr.leave'

    delegate_employee_id = fields.Many2one(
        'hr.employee',
        string='Delegate To',
        help='Employee who will handle responsibilities during leave',
        tracking=True
    )

    @api.constrains('employee_id', 'delegate_employee_id')
    def _check_delegate_employee(self):
        for leave in self:
            if leave.delegate_employee_id and leave.employee_id == leave.delegate_employee_id:
                raise ValidationError('You cannot delegate to yourself!')