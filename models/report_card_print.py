# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class reporte(models.AbstractModel):
    _name = 'report.england_school.report_card_print'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('england_school.report_card_print')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            }
        return report_obj.render("england_school.report_card_print",docargs)


