# -*- encoding: utf-8 -*-
##############################################################################

{
    "name": "Management School",
    "version": "1.0",
    "depends": [
        "account",
         "sale",
	"analytic",
	"hr",
	"base",
    ],
    "author": "Cesar Alejandro Rodriguez",
    "category": "Sale",
    "description": """
    """,
    'data': [
	"views/school_menus.xml",
	"views/course_view.xml",
	#"views/code_view_data.xml",
    "views/estudiante_view.xml",
	"views/section_view.xml",
	#"views/school_menus.xml",	
	#"views/asigantura_view.xml",
    ],
    #'update_xml' : [
     #       'security/groups.xml',
      #      'security/ir.model.access.csv'
    #],
    'demo': [],
    'installable': True,
}
