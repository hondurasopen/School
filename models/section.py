# -*- encoding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import Warning, RedirectWarning
from datetime import datetime, date, time, timedelta
import calendar


class Sections(models.Model):
    _name = "school.sections"

    name = fields.Char("Sección", required=True)
    course_id = fields.Many2one("school.course", "Curso", required=True)
    start_date = fields.Date("Fecha de inicio", required=True)
    end_date = fields.Date("Fecha final", required=True)
    prebasica = fields.Boolean("Pre Básica", default=False)
    maestro_guia = fields.Many2one("hr.employee", "Maestro Guia" , domain="[('maestro_guia', '=', True)]")
    description = fields.Text("Description and notes")
    state = fields.Selection([('draft', 'Borrador'), ('progress', 'En progreso'), ('cancel', 'Cancelada'), ('done', 'Finalizada')], string='Estado', default='draft')
    description = fields.Text("Observaciones generales")
    section_line = fields.One2many("school.sections.line", "section_id", "Asignaturas y maestro")
    alumnos_ids = fields.One2many("res.partner", "section_id", "Alumnos")


    _defaults = {'start_date': fields.Date.today()}

    @api.multi
    def action_section_progress(self):

        self.write({'state': 'progress'})

    @api.multi
    def action_section_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_section_done(self):
        self.write({'state': 'done'})

    @api.multi
    def action_section_draft(self):
        self.write({'state': 'draft'})

    @api.onchange("course_id")
    def onchangecurso(self):
        if self.course_id.nivel == 'prebasica' or self.course_id.nivel == 'basica':
            self.prebasica = True
        else:
            self.prebasica = False

    def asignar_clases(self):
        obj_line = self.env["school.sections.line"]
        obj_unlink = obj_line.search([('section_id', '=', self.id)])
        if self.section_line:
            for delete in obj_unlink:
                delete.unlink()

        for line in self.course_id.curso_line:
            values = {
                'section_id': self.id,
                'asignatura_id': line.asignatura_id.id,
                'name': line.name,
            }
            if line.asignatura_id.home_teacher and self.maestro_guia:
                values["maestro_id"] = self.maestro_guia.id

            id_section = obj_line.create(values)


class SectionsLine(models.Model):
    _name = "school.sections.line"

    section_id = fields.Many2one("school.sections", "Section", required=True)
    maestro_id = fields.Many2one("hr.employee", "Catedratico")
    asignatura_id = fields.Many2one("school.asignatura", "Asignatura")
    name = fields.Char("Descripción")
