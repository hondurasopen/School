# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
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
    descripcion = fields.Text("Observaciones generales")


    @api.onchange("student_id")
    def onchangeestudiante(self):
        if self.student_id:
            if self.student_id.section_id:
                self.section_id = self.student_id.section_id.id
                self.grade_id = self.section_id.course_id.id
            else:
                raise Warning(_('El estudiante no tiene sección asignada'))

    def generar_notas(self):
        obj_line_notas = self.env["school.notas.line"].search([('alumno_id', '=', self.student_id.id), ('section_id', '=', self.section_id.id)])
        obj_line_report_line_id = self.env["school.report.card.line"]
        obj_unlink = obj_line_report_line_id.search([('report_card_id', '=', self.id)])
        alumno_nota_obj = self.env["school.report.card"].search([('student_id', '=', self.student_id.id), ('id', '!=', self.id)])

        if alumno_nota_obj:
            raise Warning(_('El alunno seleccionado ya tiene registros de notas'))

        for delete in obj_unlink:
                delete.unlink()

        if not obj_line_notas:
            raise Warning(_('No se encuentran registros para este estudiante'))

        for section_line in self.section_id:
        for line in obj_line_notas:
            values = {
                'report_card_id': self.id,
                'clase_id': line.asignatura_id.id,
                'nota_parcial1': line.nota_parcial1,
                'nivelacion_1': line.nivelacion_1,
                'nota_parcial2': line.nota_parcial2,
                'nivelacion_2': line.nivelacion_2,
                'nota_parcial3': line.nota_parcial3,
                'nivelacion_3': line.nivelacion_3,
                'nota_parcial4': line.nota_parcial4,
                'nivelacion_4': line.nivelacion_4,
            }
            id_section = obj_line_report_line_id.create(values)



class Reportcardline(models.Model):
    _name = "school.report.card.line"

    report_card_id = fields.Many2one("school.report.card", "Boleta")
    clase_id = fields.Many2one("school.asignatura", "Asignatura")
    nota_parcial1 = fields.Float("Nota Parcial 1")
    nivelacion_1 = fields.Float("Nota Nivelación")
    nota_parcial2 = fields.Float("Nota Parcial 2")
    nivelacion_2 = fields.Float("Nota Nivelación")
    nota_parcial3 = fields.Float("Nota Parcial 3")
    nivelacion_3 = fields.Float("Nota Nivelación")
    nota_parcial4 = fields.Float("Nota Parcial 4")
    nivelacion_4 = fields.Float("Nota Nivelación")


