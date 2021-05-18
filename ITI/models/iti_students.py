from odoo import models, fields, api
from odoo.exceptions import UserError


class ItiStudent(models.Model):
    _name = "iti.student"

    @api.depends("salary")
    def calc_salary(self):
        for std in self:
            std.tax = std.salary * 0.20
            std.net_salary = std.salary - std.tax

    name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute="calc_salary", store=True)
    net_salary = fields.Float(compute="calc_salary", store=True)
    address = fields.Text()
    gender = fields.Selection([("m", 'Male'), ("f", "Female")])
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one("iti.track")
    track_capacity = fields.Integer(related="track_id.capacity")
    skills_ids = fields.Many2many("iti.skill")
    grade_ids = fields.One2many("student.course.line", "student_id")
    state = fields.Selection([
        ('applied', 'Applied'),
        ('first', 'First interview'),
        ('second', 'Second interview'),
        ('passed', 'Passed'),
        ('rejected', 'Rejected'),
    ], default='applied')

    @api.constrains("salary")
    def check_salary(self):
        if self.salary > 10000:
            raise UserError("salary can't greater than 10000")

    """
    @api.constrains("track_id")
    def check_track_id(self):
        track_count = len(self.track_id.student_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("track is full")
    """

    @api.model
    def create(self, vals):
        name_split = vals['name'].split()
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        # if email already exist for this student raise Error
        # function search
        search_student = self.search([('email', '=', vals['email'])], limit=5, offset=5)
        # track = self.env['iti.track'].browse(vals['track_id'])
        # if track.is_open is False:
        # raise UserError("selected track is closed")
        if search_student:
            raise UserError("Email already exist")
        return super().create(vals)

    def write(self, vals):
        if "name" in vals:
            name_split = vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        super().write(vals)

    def unlink(self):
        for record in self:
            if record.state in ['passed', 'rejected']:
                raise UserError("you can't delete passed/rejected students")
        super().unlink()

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed', 'rejected']:
            self.state = 'applied'

    def set_passed(self):
        self.state = 'passed'

    def set_rejected(self):
        self.state = 'rejected'

    @api.onchange("gender")
    def _on_change_gender(self):
        domain = {'track_id': []}
        if not self.gender:
            self.gender = 'm'
            return {}
        if self.gender == 'm':
            domain = {'track_id': [('is_open', '=', True)]}
            self.salary = 10000
        else:
            self.salary = 5000
        return {
            'warning': {
                'title': 'warning message',
                'message': 'please attention salary will be changed !!'
            },
            'domain': domain
        }


class ItiCourse(models.Model):
    _name = "iti.course"
    name = fields.Char()


class StudentCourseGrades(models.Model):
    _name = "student.course.line"

    student_id = fields.Many2one("iti.student")
    course_id = fields.Many2one("iti.course")
    grade = fields.Selection([
        ("G", "Good"),
        ("VG", "Very Good"),
        ("E", "Excellent")
    ])
