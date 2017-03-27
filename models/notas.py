# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
from odoo.exceptions import Warning


class NotasAlumno(models.Model):
    _name = "school.notas"
    _inherit = ['mail.thread']

    descripcion = fields.Text("Notas generales")
    seccion_id = fields.Many2one("school.sections", "Sección")
    section_media_id = fields.Many2one("school.sections", "Sección")
    maestro_id = fields.Many2one("hr.employee", "Maestro", required=True, domain=[('es_catadratico', '=', True)])
    nota_line_ids = fields.One2many("school.notas.line", "nota_id", "Calificación de alumnos")
    state = fields.Selection([('draft', 'Borrador'), ('progress', 'En progreso'), ('done', 'Finalizado')], 
        string='Estado', default='draft')
    alumno_id = fields.Many2one("res.partner", "Alumno", domain=[('es_estudiante', '=', True)])
    prebasica = fields.Boolean("Pre Básica", default=False)
    nivel_grado = fields.Selection([('prebasica', 'Pre-Básica'), ('basica', 'Básica'), ('media', 'Media')], required=True)

    @api.onchange("seccion_id")
    def onchangesecction(self):
        if self.seccion_id.prebasica:
            self.prebasica = True
            self.nivel = self.seccion_id.course_id.nivel
        else:
            self.prebasica = False
            self.nivel = self.seccion_id.course_id.nivel

    @api.onchange("maestro_id")
    def onchangemaestro(self):
        if self.maestro_id.maestro_guia:
            self.prebasica = True
        else:
            self.prebasica = False

    @api.multi
    def action_nota_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_nota_done(self):
        self.write({'state': 'done'})

    @api.multi
    def action_nota_progress(self):
        self.write({'state': 'progress'})

    # TODO: Aqui me quede
    def registrar_notas(self):
        obj_line = self.env["school.notas.line"]
        obj_unlink = obj_line.search([('nota_id', '=', self.id)])
        if self.nota_line_ids:
            for delete in obj_unlink:
                delete.unlink()

        obj_section_line = self.env["school.sections.line"].search([('section_id', '=', self.seccion_id.id), 
            ('maestro_id', '=', self.maestro_id.id)])

        if not obj_section_line:
            raise Warning(_('Maestro no tiene clases en esta sección'))

        obj_partner = self.env["res.partner"].search([('section_id', '=', self.seccion_id.id)])

        for partner in obj_partner:
            for line in obj_section_line:
                values = {
                    'nota_id': self.id,
                    'asignatura_id': line.asignatura_id.id,
                    'alumno_id': partner.id,
                }
                id_section = obj_line.create(values)


class NotasAlumnoline(models.Model):
    _name = "school.notas.line"

    nota_id = fields.Many2one("school.notas", "Notas")
    asignatura_id = fields.Many2one("school.asignatura", "Asignatura")
    alumno_id = fields.Many2one("res.partner", "Alumno", domain=[('es_estudiante', '=', True)])
    nota_parcial1 = fields.Float("Nota Parcial 1")
    nivelacion_1 = fields.Float("Nota Nivelación")
    nota_parcial2 = fields.Float("Nota Parcial 2")
    nivelacion_2 = fields.Float("Nota Nivelación")
    nota_parcial3 = fields.Float("Nota Parcial 3")
    nivelacion_3 = fields.Float("Nota Nivelación")
    nota_parcial4 = fields.Float("Nota Parcial 4")
    nivelacion_4 = fields.Float("Nota Nivelación")
    partipacion = fields.Selection([('E', 'Excelente'), ('MB', 'Muy Bueno'), ('S', 'Satisfactoria'), ('NS', 'No Satisfactoria')], string='Participación')