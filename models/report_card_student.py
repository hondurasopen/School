# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class Reportcard(models.Model):
    _name = "school.report.card"
    _inherit = ['mail.thread']

    student_id = fields.Many2one("res.partner", "Alumno", domain="[('es_estudiante', '=', True)]", required=True)
    grade_id = fields.Many2one("school.course", "Curso", required=True)
    section_id = fields.Many2one("school.sections", "Sección", required=True)
    parcial = fields.Selection([('primer', 'Primer Parcial'), ('segundo', 'Segundo Parcial'), ('tercer', 'Tercer Parcial'), ('Cuarto', 'Cuarto Parcial')], 
        string='Parcial')
    report_card_ids = fields.One2many("school.report.card.line", "report_card_id", "Detalle de calificaciones")
    maestro_guia = fields.Many2one("hr.employee", "Maestro Guia" , domain="[('maestro_guia', '=', True)]")
    promedio_parcial1 = fields.Float("Promedio Parcial 1")
    promedio_parcial2 = fields.Float("Promedio Parcial 2")
    promedio_parcial3 = fields.Float("Promedio Parcial 3")
    promedio_parcial4 = fields.Float("Promedio Parcial 4")
    comentarios_parcial_4 = fields.Text("Comentarios cuarto parcial")
    comentarios_parcial_1 = fields.Text("Comentarios primer parcial")
    comentarios_parcial_2 = fields.Text("Comentarios segundo parcial")
    comentarios_parcial_3 = fields.Text("Comentarios tercer parcial")
    comportamiento_ids = fields.One2many("school.notas.line.comportamiento", "report_card_id", "Sociabilidad y Comportamiento")
    inasistencias_1 = fields.Integer("Inasistencia I Parcial")
    inasistencias_2 = fields.Integer("Inasistencia II Parcial")
    inasistencias_3 = fields.Integer("Inasistencia III Parcial")
    inasistencias_4 = fields.Integer("Inasistencia IV Parcial")
    llegadas_1 = fields.Integer("Llegadas Tarde I Parcial")
    llegadas_2 = fields.Integer("Llegadas Tarde II Parcial")
    llegadas_3 = fields.Integer("Llegadas Tarde III Parcial")
    llegadas_4 = fields.Integer("Llegadas Tarde IV Parcial")

    @api.onchange("student_id")
    def onchangeestudiante(self):
        if self.student_id:
            if self.student_id.section_id:
                self.section_id = self.student_id.section_id.id
                self.grade_id = self.section_id.course_id.id
                self.maestro_guia = self.section_id.maestro_guia.id
            else:
                raise Warning(_('El estudiante no tiene sección asignada'))

    def generarpromedios(self):
        nota_parcial = 0.0
        nota_parcial2 = 0.0
        nota_parcial3 = 0.0
        nota_parcial4 = 0.0
        num_clases = 0
        if self.parcial == 'primer' or not self.parcial:
            for nota in self.report_card_ids:
                if nota.clase_id.area_asignatura != 'sociabilidad':
                    nota_parcial += nota.nota_parcial1
                    nota_parcial2 += nota.nota_parcial2
                    nota_parcial3 += nota.nota_parcial3
                    nota_parcial4 += nota.nota_parcial3
                    num_clases += 1
            if num_clases > 0:
                self.promedio_parcial1 = nota_parcial / num_clases
                self.promedio_parcial2 = nota_parcial2 / num_clases
                self.promedio_parcial3 = nota_parcial3 / num_clases
                self.promedio_parcial4 = nota_parcial4 / num_clases

    def generar_notas(self):
        obj_line_comportamiento = self.env["school.notas.line.comportamiento"]
        obj_line_notas = self.env["school.notas.line"].search([('alumno_id', '=', self.student_id.id), ('section_id', '=', self.section_id.id)])
        obj_nota = self.env["school.notas"].search([('alumno_id', '=', self.student_id.id), ('seccion_id', '=', self.section_id.id)], limit=1)
        obj_line_report_line_id = self.env["school.report.card.line"]
        obj_unlink = obj_line_report_line_id.search([('report_card_id', '=', self.id)])
        alumno_nota_obj = self.env["school.report.card"].search([('student_id', '=', self.student_id.id), ('id', '!=', self.id)])
        id_section = False
        if alumno_nota_obj:
            raise Warning(_('El alunno seleccionado ya tiene registros de notas'))

        for delete in obj_unlink:
                delete.unlink()

        if not obj_line_notas:
            raise Warning(_('No se encuentran registros para este estudiante'))

        for section_line in self.section_id.section_line:
            values = {
                'report_card_id': self.id,
                'clase_id': section_line.asignatura_id.id,
            }
            for line in obj_line_notas:
                if section_line.asignatura_id.id == line.asignatura_id.id:
                    values["total_1"] = line.nota_parcial1
                    values["nivelacion_1"] = line.nivelacion_1
                    values["nota_parcial1"] = line.nota_parcial1 + line.nivelacion_1

                    values["total_2"] = line.nota_parcial2
                    values["nivelacion_2"] = line.nivelacion_2
                    values["nota_parcial2"] = line.nota_parcial2 + line.nivelacion_2

                    values["total_3"] = line.nota_parcial3
                    values["nivelacion_3"] = line.nivelacion_3
                    values["nota_parcial3"] = line.nota_parcial3 + line.nivelacion_3

                    values["total_4"] = line.nota_parcial4
                    values["nivelacion_4"] = line.nivelacion_4
                    values["nota_parcial4"] = line.nota_parcial4 + line.nivelacion_4

            id_section = obj_line_report_line_id.create(values)

        if id_section and self.section_id.prebasica:
            comp_ids = obj_line_comportamiento.search([('section_id', '=', self.section_id.id), ('alumno_id', '=', self.student_id.id)])
            if comp_ids:
                for obj_ids in comp_ids:
                    obj_ids.write({'report_card_id': self.id})
            self.comentarios_parcial_1 = obj_nota.comentarios_1
            self.inasistencias_1 = obj_nota.inasistencias_1
            self.llegadas_1 = obj_nota.inasistencias_1
            self.comentarios_parcial_2 = obj_nota.comentarios_2
            self.inasistencias_2 = obj_nota.inasistencias_2
            self.llegadas_2 = obj_nota.inasistencias_2
            self.comentarios_parcial_3 = obj_nota.comentarios_3
            self.inasistencias_3 = obj_nota.inasistencias_3
            self.llegadas_3 = obj_nota.inasistencias_3
            self.comentarios_parcial_4 = obj_nota.comentarios_4
            self.inasistencias_4 = obj_nota.inasistencias_4
            self.llegadas_4 = obj_nota.inasistencias_4
            self.generarpromedios()



class Reportcardline(models.Model):
    _name = "school.report.card.line"

    report_card_id = fields.Many2one("school.report.card", "Boleta")
    clase_id = fields.Many2one("school.asignatura", "Asignatura", required=True)
    nota_parcial1 = fields.Float("Nota Parcial 1")
    nivelacion_1 = fields.Float("Nota Nivelación")
    total_1 = fields.Float("Total")
    nota_parcial2 = fields.Float("Nota Parcial 2")
    nivelacion_2 = fields.Float("Nota Nivelación")
    total_2 = fields.Float("Total")
    nota_parcial3 = fields.Float("Nota Parcial 3")
    nivelacion_3 = fields.Float("Nota Nivelación")
    total_3 = fields.Float("Total")
    nota_parcial4 = fields.Float("Nota Parcial 4")
    nivelacion_4 = fields.Float("Nota Nivelación")
    total_4 = fields.Float("Total")

