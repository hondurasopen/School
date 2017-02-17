# -*- encoding: utf-8 -*-
from openerp import models, fields, api 
class Topic(models.Model):
	_name = "school.notas"
	
	name=fields.Char("Name of Topic", required= True )
	descripcion = fields.Char("Descripción de asignatura")
	
		


        

