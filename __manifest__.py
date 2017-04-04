# -*- encoding: utf-8 -*-
##############################################################################
{
    "name": "Management School",
    "version": "1.0",
    "depends": [
    	"account",
        "sale",
		"mail",
		"analytic",
		"hr",
		"base",
    ],
    "author": "Cesar Alejandro Rodriguez",
    "category": "Sale",
    "description": """
    """,
    'data': [
	"security/groups.xml",
    "security/ir.model.access.csv",
	"views/school_menus.xml",
	"views/course_view.xml",
	"views/asignatura_view.xml",
	"views/hr_catedratico.xml",
    "views/estudiante_view.xml",
	"views/section_view.xml",
	#"views/school_menus.xml",	
	"views/notas_view.xml",
	"views/report_card_view.xml",
	"reports/report_card_print.xml",
	"reports/report_card_print_view.xml",
    ],
    #'update_xml' : [
     #       'security/groups.xml',
      #      'security/ir.model.access.csv'
    #],
    'demo': [],
    'installable': True,
}
