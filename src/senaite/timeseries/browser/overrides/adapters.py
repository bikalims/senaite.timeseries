# -*- coding: utf-8 -*-

from bika.lims import api

# from bika.lims.interfaces import IAnalysisService
from senaite.core.browser.form.adapters.analysisservice import EditForm
from senaite.core.interfaces import IAjaxEditForm
from zope.interface import implementer


@implementer(IAjaxEditForm)
class AnalysisServiceEditForm(EditForm):
    def __init__(self, context, request):
        import pdb; pdb.set_trace()  # fmt: skip

    def toggle_result_type(self, result_type):
        """Hides/Show result options depending on the result type"""
        import pdb; pdb.set_trace()  # fmt: skip
        if result_type and api.is_list(result_type):
            return self.toggle_result_type(result_type[0])

        if result_type in ["numeric", "string", "text"]:
            self.add_hide_field("ResultOptions")
            self.add_hide_field("ResultOptionsSorting")
            self.add_hide_field("GraphTitle")
            self.add_hide_field("GraphXAxisTitle")
            self.add_hide_field("GraphYAxisTitle")
        elif result_type == "timeseries":
            self.add_hide_field("ResultOptions")
            self.add_hide_field("ResultOptionsSorting")
            self.add_show_field("GraphTitle")
            self.add_show_field("GraphXAxisTitle")
            self.add_show_field("GraphYAxisTitle")
        else:
            self.add_show_field("ResultOptions")
            self.add_show_field("ResultOptionsSorting")
            self.add_hide_field("GraphTitle")
            self.add_hide_field("GraphXAxisTitle")
            self.add_hide_field("GraphYAxisTitle")

    def can_change_keyword(self, keyword):
        return self.can_change_keyword(str(keyword))
