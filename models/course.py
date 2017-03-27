# -*- encoding: utf-8 -*-
from openerp import models, fields, api 


class Course(models.Model):
    _name = "school.course"
    _inherit = ['mail.thread']

    name = fields.Char("Nombre del grado", required=True)
    description = fields.Text("Descripción del grado")
    activo = fields.Boolean("Curso activo", default=True)
    nivel = fields.Selection([('prebasica', 'Pre-Básica'), ('basica', 'Básica'), ('media', 'Media')], required=True)
    section_ids = fields.One2many("school.sections", "course_id", "Secciones")
    curso_line = fields.One2many("school.course.line", "curso_id", "Detalles del grado")
    home_teacher = fields.Boolean("Maestro Guia")


class CursoLine(models.Model):
    _name = "school.course.line"

    curso_id = fields.Many2one("school.course", "Section")
    # maestro_id = fields.Many2one("hr.employee", "Catedratico")
    asignatura_id = fields.Many2one("school.asignatura", "Asignatura", required=True)
    name = fields.Char("Descripción")

    @api.onchange("asignatura_id")
    def onchangeasignatura(self):
        if self.asignatura_id.area_asignatura == 'comunicacion':
            self.name = 'Área de comunicación'
        elif self.asignatura_id.area_asignatura == 'matematicas':
            self.name = 'Área de matemáticas'
        elif self.asignatura_id.area_asignatura == 'ciencias':
            self.name = 'Área de ciencias naturales'
        else:
            self.name =  'Área de ciencias sociales'
