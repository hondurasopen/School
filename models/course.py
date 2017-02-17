# -*- encoding: utf-8 -*-
from openerp import models, fields, api 


class Course(models.Model):
    _name = "school.course"

    name = fields.Char("Nombre de curso", required=True)
    description = fields.Text("Descripción de curso")
    activo = fields.Boolean("Curso activo", default=True)
    section_ids = fields.One2many("school.sections", "course_id", "Secciones")

