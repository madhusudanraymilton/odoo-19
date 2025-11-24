from odoo import api, fields, models

class Enrollment(models.Model):
    _name = 'student.enrollment'
    _description = 'Student Enrollment'

    name = fields.Char(string="Name")
    marks = fields.Float(string="Marks")

    className = fields.Selection([
        ('bsc', 'BSC'),
        ('bba', 'BBA'),
        ('ba', 'BA'),
        ('cse', 'CSE'),
    ], string="Department")

    grade = fields.Text(string="Grade", compute="_compute_grade")

    @api.depends('marks')
    def _compute_grade(self):
        for record in self:
            if record.marks >= 90:
                record.grade = 'A+'
            elif record.marks >= 80:
                record.grade = 'B+'
            elif record.marks >= 70:
                record.grade = 'C+'
            elif record.marks >= 60:
                record.grade = 'D+'
            elif record.marks <= 33:
                record.grade = 'F'
