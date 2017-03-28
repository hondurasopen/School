# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
from odoo.exceptions import Warning


class NotasAlumno(models.Model):
    _name = "school.notas"
    _inherit = ['mail.thread']

    descripcion = fields.Text("Notas generales")
    seccion_id = fields.Many2one("school.sections", "Sección")
    section_media_id = fields.Many2one("school.sections", "Sección")
    maestro_id = fields.Many2one("hr.employee", "Maestro", required=True, domain="[('es_catadratico', '=', True)]")
    nota_line_ids = fields.One2many("school.notas.line", "nota_id", "Calificación de alumnos")
    state = fields.Selection([('draft', 'Borrador'), ('progress', 'En evaluación'), ('done', 'Finalizado')], 
        string='Estado', default='draft')
    alumno_id = fields.Many2one("res.partner", "Alumno", domain="[('es_estudiante', '=', True)]")
    prebasica_nota = fields.Boolean("Pre Básica", default=False)
    nivel_section = fields.Selection([('prebasica', 'Pre-Básica'), ('basica', 'Básica'), ('media', 'Media')], required=True)

    @api.onchange("seccion_id")
    def onchangesecction(self):
        if self.seccion_id.prebasica:
            self.prebasica_nota = True
            self.nivel_section = self.seccion_id.course_id.nivel
        else:
            self.prebasica_nota = False
            self.nivel_section = self.seccion_id.course_id.nivel

    @api.onchange("section_media_id")
    def onchangesecctionmedia(self):
        self.prebasica_nota = False
        self.nivel_section = self.section_media_id.course_id.nivel

    @api.onchange("maestro_id")
    def onchangemaestro(self):
        if self.maestro_id.maestro_guia:
            self.prebasica_nota = True
        else:
            self.prebasica_nota = False

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
        obj_partner = False
        obj_section_line = False
        if self.nota_line_ids:
            for delete in obj_unlink:
                delete.unlink()

        if self.seccion_id:
            obj_section_line = self.env["school.sections.line"].search([('section_id', '=', self.seccion_id.id), 
            ('maestro_id', '=', self.maestro_id.id)])
        else:
            obj_section_line = self.env["school.sections.line"].search([('section_id', '=', self.section_media_id.id), 
            ('maestro_id', '=', self.maestro_id.id)])

        if not obj_section_line:
            raise Warning(_('Maestro no tiene clases en esta sección'))

        if self.prebasica_nota and self.seccion_id:
            obj_partner = self.env["res.partner"].search([('section_id', '=', self.seccion_id.id), ('id', '=', self.alumno_id.id)])
            alumno_nota_obj = self.env["school.notas"].search([('alumno_id', '=', self.alumno_id.id), 
                ('maestro_id', '=', self.maestro_id.id),('id', '!=', self.id)])
            if alumno_nota_obj:
                raise Warning(_('El alunno seleccionado ya tiene registros de notas'))

        elif self.section_media_id:
            obj_partner = self.env["res.partner"].search([('section_id', '=', self.section_media_id.id)])
            alumno_nota_obj = self.env["school.notas"].search([('section_media_id', '=', self.section_media_id.id), 
                ('maestro_id', '=', self.maestro_id.id),('id', '!=', self.id)])
            if alumno_nota_obj:
                raise Warning(_('Ya se encuentra un registro con la sección que se esta seleccionado'))
        else:
            raise Warning(_('Consulte al adminstrador del sistema respecto a este error'))

        if not obj_partner:
            raise Warning(_('Alumno no es de esta sección'))

        for partner in obj_partner:
            for line in obj_section_line:
                values = {
                    'nota_id': self.id,
                    'asignatura_id': line.asignatura_id.id,
                    'alumno_id': partner.id,
                }
                if self.seccion_id:
                    values["section_id"] = self.seccion_id.id
                if self.section_media_id:
                    values["section_id"] = self.section_media_id.id
                id_section = obj_line.create(values)


class NotasAlumnoline(models.Model):
    _name = "school.notas.line"

    nota_id = fields.Many2one("school.notas", "Notas")
    asignatura_id = fields.Many2one("school.asignatura", "Asignatura")
    alumno_id = fields.Many2one("res.partner", "Alumno", domain=[('es_estudiante', '=', True)])
    section_id = fields.Many2one("school.sections", "Sección")
    nota_parcial1 = fields.Float("Nota Parcial 1")
    nivelacion_1 = fields.Float("Nota Nivelación")
    nota_parcial2 = fields.Float("Nota Parcial 2")
    nivelacion_2 = fields.Float("Nota Nivelación")
    nota_parcial3 = fields.Float("Nota Parcial 3")
    nivelacion_3 = fields.Float("Nota Nivelación")
    nota_parcial4 = fields.Float("Nota Parcial 4")
    nivelacion_4 = fields.Float("Nota Nivelación")
    partipacion = fields.Selection([('E', 'Excelente'), ('MB', 'Muy Bueno'), ('S', 'Satisfactoria'), ('NS', 'No Satisfactoria')], string='Participación')