# -*- encoding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import Warning, RedirectWarning
from datetime import datetime, date, time, timedelta
import calendar


class Sections(models.Model):
    _name = "school.sections"

    name = fields.Char("Seccion", required=True)
    course_id = fields.Many2one("school.course", "Curso", required=True)
    start_date = fields.Date("Fecha de inicio", required=True)
    end_date = fields.Date("Fecha final")
    description = fields.Text("Description and notes")
    state = fields.Selection([('draft', 'Borrador'), ('progress', 'En progreso'), ('cancel', 'Cancelada'), ('done', 'Finalizada')], string='Estado', default='draft')
    description = fields.Text("Observaciones generales")
    section_line = fields.One2many("school.sections.line", "section_id", "Asignaturas y maestro")

    _defaults = {'start_date': fields.Date.today()}


class SectionsLine(models.Model):
    _name = "school.sections.line"

    section_id = fields.Many2one("school.sections", "Section")
    maestro_id = fields.Many2one("hr.employee", "Catedratico")
    asignatura_id = fields.Many2one("school.asignatura", "Asignatura")
    name = fields.Char("Descripción")


class SectionsAsignturas(models.Model):
    _name = "school.asignatura"

    name = fields.Char("Nombre de asigantura")
    description = fields.Text("Descripción de asignatura")
