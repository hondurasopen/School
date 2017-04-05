# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
from odoo.exceptions import Warning


class NotasAlumno(models.Model):
    _name = "school.notas"
    _inherit = ['mail.thread']

    @api.model
    def getmaestro(self):
        obj_maestro = self.env["hr.employee"].search([('user_id', '=', self.env.user.id)])
        if obj_maestro:
            return obj_maestro

    nivel_escolar = fields.Selection([('prebasica', 'Pre School Level 1'), ('prebasica2', 'Pre School Level 2'), ('prebasica3', 'Pre School Level 3'),('basica', 'Elementary Level 1'),
        ('media', 'Middle School'), ('media2', 'High School 10th'), ('media3', 'High School 11th')])
    comentarios_1 = fields.Text("Notas generales")
    comentarios_2 = fields.Text("Notas generales")
    comentarios_3 = fields.Text("Notas generales")
    comentarios_4 = fields.Text("Notas generales")
    seccion_id = fields.Many2one("school.sections", "Sección Primaria/Pre-básica")
    section_media_id = fields.Many2one("school.sections", "Sección")
    maestro_id = fields.Many2one("hr.employee", "Maestro", required=True, domain="[('es_catadratico', '=', True)]", default= getmaestro)
    nota_line_ids = fields.One2many("school.notas.line", "nota_id", "Calificación de alumnos")
    state = fields.Selection([('draft', 'Borrador'), ('progress', 'En evaluación'), ('done', 'Finalizado')], 
        string='Estado', default='draft')
    alumno_id = fields.Many2one("res.partner", "Alumno", domain="[('es_estudiante', '=', True)]")
    prebasica_nota = fields.Boolean("Pre Básica", default=False)
    comportamiento_ids = fields.One2many("school.notas.line.comportamiento","nota_id","Sociabilidad y Comportamiento")
    maestro_guia = fields.Boolean("Es maestro guia")
    inasistencias_1 = fields.Integer("Inasistencia I Parcial")
    inasistencias_2 = fields.Integer("Inasistencia II Parcial")
    inasistencias_3 = fields.Integer("Inasistencia III Parcial")
    inasistencias_4 = fields.Integer("Inasistencia IV Parcial")
    llegadas_1 = fields.Integer("Llegadas Tarde I Parcial")
    llegadas_2 = fields.Integer("Llegadas Tarde II Parcial")
    llegadas_3 = fields.Integer("Llegadas Tarde III Parcial")
    llegadas_4 = fields.Integer("Llegadas Tarde IV Parcial")

    @api.onchange("seccion_id")
    def onchangesecction(self):
        if self.seccion_id:
            if self.seccion_id.prebasica:
                self.prebasica_nota = True
                self.nivel_escolar = self.seccion_id.course_id.nivel
                if self.seccion_id.maestro_guia.id == self.maestro_id.id:
                    self.maestro_guia = True

            else:
                self.prebasica_nota = False
                self.nivel_escolar = self.seccion_id.course_id.nivel

    @api.onchange("section_media_id")
    def onchangesecctionmedia(self):
        if self.section_media_id:
            self.prebasica_nota = False
            self.nivel_escolar = self.section_media_id.course_id.nivel

    @api.onchange("maestro_id")
    def onchangemaestro(self):
        if self.maestro_id:
            if self.maestro_id.maestro_guia:
                self.prebasica_nota = True
                self.maestro_guia = True
            else:
                self.prebasica_nota = False
                self.maestro_guia = False

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
        id_line_notas = False
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
                id_line_notas = obj_line.create(values)

        if id_line_notas and self.prebasica_nota:
            obj_line = self.env["school.notas.line.comportamiento"]
            obj_comportamiento = self.env["school.asignatura.comportamiento"].search([('id', '!=', 0)])
            obj_unlink = obj_line.search([('nota_id', '=', self.id)])
            if self.comportamiento_ids:
                for delete in obj_unlink:
                    delete.unlink()

            for comportamiento in obj_comportamiento:
                valores = {
                    'comportamiento_id': comportamiento.id,
                    'alumno_id': self.alumno_id.id,
                    'section_id': self.seccion_id.id,
                    'nota_id': self.id,
                }
                id_com = obj_line.create(valores)


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

class NotasComportamiento(models.Model):
    _name = "school.notas.line.comportamiento"

    nota_id = fields.Many2one("school.nota", "Nota Id")
    report_card_id = fields.Many2one("school.report.card", "Report Card")
    section_id = fields.Many2one("school.sections", "Sección Id")
    alumno_id = fields.Many2one("res.partner", "Alumno", domain=[('es_estudiante', '=', True)])
    comportamiento_id = fields.Many2one("school.asignatura.comportamiento", "Sociabilidad y Comportamiento")
    partipacion_4 = fields.Selection([('E', 'Excelente'), ('MB', 'Muy Bueno'), ('S', 'Satisfactoria'), ('NS', 'No Satisfactoria')], string='Participación IV Parcial')
    partipacion_3 = fields.Selection([('E', 'Excelente'), ('MB', 'Muy Bueno'), ('S', 'Satisfactoria'), ('NS', 'No Satisfactoria')], string='Participación III Parcial')
    partipacion_2 = fields.Selection([('E', 'Excelente'), ('MB', 'Muy Bueno'), ('S', 'Satisfactoria'), ('NS', 'No Satisfactoria')], string='Participación II Parcial')
    partipacion_1 = fields.Selection([('E', 'Excelente'), ('MB', 'Muy Bueno'), ('S', 'Satisfactoria'), ('NS', 'No Satisfactoria')], string='Participación I Parcial')
