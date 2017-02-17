
from openerp import api, models
class reporte(models.AbstractModel):
    _name = 'report.nahuiik_matricula.report_contract'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('nahuiik_matricula.report_contract')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            }
        return report_obj.render("nahuiik_matricula.report_contract",docargs)
      

