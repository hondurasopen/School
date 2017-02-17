# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta


class Estudiante(models.Model):
    _inherit= "res.partner"

    # Detalles de alumno
    es_estudiante = fields.Boolean("Es estudiante")
    fecha_nacimiento = fields.Date("Fecha de Nacimiento", translate=True)
    edad = fields.Integer("Edad de estudiante", translate=True)
    partida_nacimiento = fields.Char("Número de Identidad", required=True)
    genero = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string='Genero', required=True, translate=True)
    # Informaciión de padre
    nombre_padre = fields.Char("Padre o Encargado", translate=True)
    ocupacion_padre = fields.Char("Profesión/Ocupación de padre", translate=True)
    tel_padre = fields.Char("Telefono de padre", translate=True)
    lugar_trabajo_padre = fields.Char("Lugar de trabajo/dirección")
    email_padre = fields.Char("Correo de padre")
    direccion_padre = fields.Text("Dirección de casa de habitación")
    # Información de madre
    nombre_madre = fields.Char("Madre o Encargada", translate=True)
    ocupacion_madre = fields.Char("Profesión/Ocupación de madre", translate=True)
    tel_madre = fields.Char("Telefono de madre", translate=True)
    lugar_trabajo_madre = fields.Char("Lugar de trabajo/dirección")
    email_madre = fields.Char("Correo de Madre")
    direccion_madre = fields.Text("Dirección de casa de habitación")
    # Información de emergencia
    caso_emergencia = fields.Char("Emergencias notificar a")
    dir_emergencia = fields.Text("Dirección de contacto de emergencia")
    medico_alumno = fields.Char("Medico del alumno")
    dir_clinica = fields.Text("Dirección de clinica")
    tel_clinica = fields.Char("Telefono de clinica")

    # Información de transporte
    transporte = fields.Selection([('vehiculo', 'Automovil'), ('bus', 'Bus'), ('caminando', 'Caminando')], string='Transporte', required=True)
    persona_1 = fields.Char("Persona autorizada")
    persona_2 = fields.Char("Persona autorizada")
    persona_3 = fields.Char("Persona autorizada")
    persona_4 = fields.Char("Persona autorizada")
    persona_5 = fields.Char("Persona autorizada")
    persona_6 = fields.Char("Persona autorizada")

    # Información clinica
    panadol = fields.Boolean("Panadol (analgesico dolor y fiebre)")
    peptobismol = fields.Boolean("Peptobismol (dolores de estomago)")
    agua_oxigenada = fields.Boolean("Agua Oxigenada (cortadas)")
    anestil = fields.Boolean("Anestil (Gotas calmantes de dolor muelas y oidos)")
    neobol = fields.Boolean("Neobol (cream tópica para raspaduras)")
    mevalgin = fields.Boolean("Mevalgin (analgesico, anti-inflamatorio)")
    mucosolvan = fields.Boolean("Mucosolvan (jarabe para la tos)")
    espamotro = fields.Boolean("Espamotro-pin (nauseas, vomitos, colicos)")
    enfermedad_alumno = fields.Char("Enfermedad que padece el niño")
    otros = fields.Boolean("Otros")

    defaults = {'lang': 'es_GT', 'fecha_nacimiento': fields.Date.today()}

    @api.onchange("fecha_nacimiento")
    def calcular_edad(self):
        for x in self:
            if self.fecha_nacimiento:
                fecha_hoy = str(fields.Date.today())
                hoy = (datetime.strptime(fecha_hoy, '%Y-%m-%d'))
                edad = hoy.year - datetime.strptime(self.fecha_nacimiento, '%Y-%m-%d').year
                self.edad = edad
