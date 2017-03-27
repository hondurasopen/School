# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime,timedelta


class SectionsAsignturas(models.Model):
    _name = "school.asignatura"

    name = fields.Char("Nombre de asigantura", required=True)
    description = fields.Text("Descripción de asignatura")
    home_teacher = fields.Boolean("Maestro Guia")
    area_asignatura = fields.Selection([('comunicacion', 'Área de comunicación'), ('matematicas', 'Área de matemáticas'), 
        ('ciencias', 'Área de ciencias naturales'), ('sociales', 'Área de ciencias sociales')], string="Área", required=True)
    nivel = fields.Selection([('prebasica', 'Pre-Básica'), ('basica', 'Básica'), ('media', 'Media')], required=True, string="Nivel")
    asignatura_line = fields.One2many("school.asignatura.line", "asignatura_id", "Detalle de asignaturas")


class SectionsAsignturas(models.Model):
    _name = "school.asignatura.line"

    asignatura_id = fields.Many2one("school.asignatura", "Asignatura")
    catedratico_id = fields.Many2one("hr.employee", "Maestros", domain=[('es_catadratico', '=', True)])
    name = fields.Char("Descripción")
