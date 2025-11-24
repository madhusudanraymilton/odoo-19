from odoo import fields, models, api

class Course(models.Model):
    _name = 'student.course'
    _description = 'Student Course'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    credit = fields.Char(string="Credit")

