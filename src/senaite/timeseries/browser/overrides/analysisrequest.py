# -*- coding: utf-8 -*-

from bika.lims import api
from bika.lims.browser.analysisrequest.tables import AnalysesView as AV
from bika.lims.utils import get_image
from senaite.core import logger
from senaite.core.api import dtime
from senaite.core.permissions import ViewResults
from senaite.timeseries.config import _
from senaite.timeseries.utils import format_timeseries


class AnalysesView(AV):

    def _folder_item_result(self, analysis_brain, item):
        """Set the analysis' result to the item passed in.

        :param analysis_brain: Brain that represents an analysis
        :param item: analysis' dictionary counterpart that represents a row
        """

        item["Result"] = ""

        if not self.has_permission(ViewResults, analysis_brain):
            # If user has no permissions, don"t display the result but an icon
            img = get_image("to_follow.png", width="16px", height="16px")
            item["before"]["Result"] = img
            return

        # Get the analysis object
        obj = self.get_object(analysis_brain)

        result = obj.getResult()
        logger.info(
            "AnalysisRequestOverride::_folder_item_result: result: {}".format(result)
        )
        capture_date = obj.getResultCaptureDate()
        localized_capture_date = dtime.to_localized_time(capture_date, long_format=1)

        item["Result"] = result
        item["ResultCaptureDate"] = dtime.to_iso_format(capture_date)
        item["replace"]["ResultCaptureDate"] = localized_capture_date

        # Add the unit after the result
        unit = item.get("Unit")
        if unit:
            item["after"]["Result"] = self.render_unit(unit)

        result_type = obj.getResultType()

        # Edit mode enabled of this Analysis
        if self.is_analysis_edition_allowed(analysis_brain):
            # Allow to set Remarks
            item["allow_edit"].append("Remarks")

            if self.is_manual_result_capture_date_allowed():
                # Allow to edit the capture date, e.g. when the result was
                # captured manually after the instrument measurement.
                item["allow_edit"].append("ResultCaptureDate")

            # Set the results field editable
            if self.is_result_edition_allowed(analysis_brain):
                item["allow_edit"].append("Result")

            # Display the DL operand (< or >) in the results entry field if
            # the manual entry of DL is set, but DL selector is hidden
            allow_manual = obj.getAllowManualDetectionLimit()
            selector = obj.getDetectionLimitSelector()
            if allow_manual and not selector:
                operand = obj.getDetectionLimitOperand()
                item["Result"] = "{} {}".format(operand, result).strip()

            # Prepare result options
            item["result_type"] = result_type

            choices = self.get_result_options(obj)
            if choices:
                if result_type == "select":
                    # By default set empty as the default selected choice
                    choices.insert(0, dict(ResultValue="", ResultText=""))
                item["choices"]["Result"] = choices

            if result_type == "numeric":
                item["help"]["Result"] = _(
                    "Enter the result either in decimal or scientific "
                    "notation, e.g. 0.00005 or 1e-5, 10000 or 1e5"
                )

            if result_type == "timeseries":
                item["time_series_columns"] = obj.TimeSeriesColumns

        else:
            # Edit mode is NOT enabled of this Analysis
            if result_type == "timeseries":
                item["result_type"] = "timeseries_readonly"

        if not result:
            logger.info("AnalysisRequestOverride::_folder_item_result: no result")
            return

        formatted_result = obj.getFormattedResult(
            sciformat=int(self.scinot), decimalmark=self.dmk
        )
        item["formatted_result"] = formatted_result
        logger.info(
            "AnalysisRequestOverride::_folder_item_result: formatted_result: {}".format(
                formatted_result
            )
        )
        if result_type == "timeseries":
            item["time_series_values"] = format_timeseries(obj, result)
            item["time_series_columns"] = obj.TimeSeriesColumns
            item["time_series_graph_interpolation"] = obj.GraphInterpolation
            item["time_series_graph_title"] = obj.GraphTitle
            item["time_series_graph_xaxis"] = obj.GraphXAxisTitle
            item["time_series_graph_yaxis"] = obj.GraphYAxisTitle

    def folderitems(self):
        # This shouldn't be required here, but there are some views that calls
        # directly contents_table() instead of __call__, so before_render is
        # never called. :(
        self.before_render()

        # Get all items
        # Note we call AnalysesView's base class!
        items = super(AnalysesView, self).folderitems()
        newitems = []
        cats = []
        for item in items:
            if "result_type" not in item or not item.get("result_type").startswith(
                "timeseries"
            ):
                newitems.append(item)
                if item["category"] not in cats:
                    cats.append(item["category"])
        logger.info(
            "AnalysisRequestOverride::folderitems: found {} items with without timeseries items and {} categories".format(
                len(newitems), len(cats)
            )
        )
        self.categories = cats
        return newitems


class FieldAnalysesTable(AnalysesView):
    def __init__(self, context, request):
        super(FieldAnalysesTable, self).__init__(context, request)

        self.contentFilter.update(
            {"getPointOfCapture": "field", "getAncestorsUIDs": [api.get_uid(context)]}
        )

        self.form_id = "%s_field_analyses" % api.get_id(context)
        self.allow_edit = True
        self.show_workflow_action_buttons = True
        self.show_select_column = True
        self.show_search = False
        self.expand_all_categories = False
        self.reorder_analysis_columns()


class LabAnalysesTable(AnalysesView):
    def __init__(self, context, request):
        super(LabAnalysesTable, self).__init__(context, request)

        self.contentFilter.update(
            {"getPointOfCapture": "lab", "getAncestorsUIDs": [api.get_uid(context)]}
        )

        self.form_id = "%s_lab_analyses" % api.get_id(context)
        self.allow_edit = True
        self.show_workflow_action_buttons = True
        self.show_select_column = True
        self.show_search = False
        self.expand_all_categories = False
        self.reorder_analysis_columns()
