# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime,timedelta


class SectionsAsignturas(models.Model):
    _name = "school.asignatura"

    name = fields.Char("Nombre de asigantura", required=True)
    description = fields.Text("Descripción de asignatura")
    home_teacher = fields.Boolean("Maestro Guia")
    area_asignatura = fields.Selection([('comunicacion', 'Área de comunicación'), ('matematicas', 'Área de matemáticas'), 
        ('ciencias', 'Área de ciencias naturales'), ('sociales', 'Área de ciencias sociales'), ('sociabilidad', 'Sociabilidad y comportamiento')], string="Área", required=True)
    nivel = fields.Selection([('prebasica', 'Pre School Level 1'), ('prebasica2', 'Pre School Level 2'), ('prebasica3', 'Pre School Level 3'),('basica', 'Elementary Level 1'),
        ('media', 'Middle School'), ('media2', 'High School 10th'), ('media3', 'High School 11th')], required=True, string="Nivel")
    asignatura_line = fields.One2many("school.asignatura.line", "asignatura_id", "Detalle de asignaturas")


class SectionsAsignturas(models.Model):
    _name = "school.asignatura.line"

    asignatura_id = fields.Many2one("school.asignatura", "Asignatura")
    catedratico_id = fields.Many2one("hr.employee", "Maestros", domain=[('es_catadratico', '=', True)])
    name = fields.Char("Descripción")


class Comportamiento(models.Model):
    _name = "school.asignatura.comportamiento"

    name = fields.Char("Sociabilidad y Comportamiento")