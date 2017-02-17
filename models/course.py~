# -*- encoding: utf-8 -*-
from openerp import models, fields, api 
class Course(models.Model):
	_name="mngfees.course"	

	name=fields.Char("Course Name", required= True )
	code= fields.Char("Course Code")
	price= fields.Float("Course Price")
	duration= fields.Float("Duration")
	description= fields.Text("Description and notes")
	active= fields.Boolean("Active Course", default= True)
	section_ids= fields.One2many("mngfees.sections", "course_id", "Sections")
	product_cat_id= fields.Many2one("product.category","Product Category", required= True)
	contract_id = fields.Many2one("mngfees.contractsale","Contract id")
		

	@api.model
	def create(self,vals):
		
		obj_product= self.env["product.product"]
		values={
			'name':vals.get("name"),
			'lst_price':vals.get("price"),
			'default_code': vals.get("code"),
			'type': 'service',
			'categ_id': vals.get("product_cat_id"),
			}
		obj_product.create(values)
		return super(Course,self).create(vals)

	#TODO: Allan Validar cada campo que se rescribira en el product.product
	@api.multi
	def write(self,vals):
		obj_product=self.env["product.product"].search([("default_code","=",vals.get("code"))])
		values={
			'name':vals.get("name"),		
			'lst_price':vals.get("price"),
			'default_code': vals.get("code"),
			'type': 'service',
			'categ_id': vals.get("product_cat_id"),
			}
		obj_product.write(values)
		return super(Course,self).write(vals)




        

