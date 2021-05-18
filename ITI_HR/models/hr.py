from odoo import models, fields


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    salary = fields.Float()
    military_certificate = fields.Binary()
