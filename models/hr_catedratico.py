# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime,timedelta


class Catedratico(models.Model):
    _inherit= "hr.employee"

    es_catadratico = fields.Boolean("Es catedrático")
    maestro_guia = fields.Boolean("Maestro de primaria")
    maestro_especial = fields.Boolean("Maestro Especial")