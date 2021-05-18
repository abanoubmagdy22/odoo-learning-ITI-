from odoo import models, fields


class ItiTrack(models.Model):
    _name = "iti.track"

    # _rec_name="capacity"
    name = fields.Char()
    is_open = fields.Boolean()
    capacity = fields.Integer()
    student_ids = fields.One2many("iti.student", "track_id")
