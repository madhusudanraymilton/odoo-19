from odoo import api, fields, models

class Student(models.Model):
    _name = "student.student"
    _description = "Student"

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")