# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.TIMESERIES.
#
# SENAITE.TIMESERIES is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020-2024 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from senaite.core import logger
from senaite.core.browser.viewlets.sampleanalyses import LabAnalysesViewlet
from senaite.timeseries.config import is_installed
from senaite.timeseries.config import _
from senaite.timeseries.browser.overrides.analysisrequest import AnalysesView


class TimeSeriesAnalysesViewlet(LabAnalysesViewlet):
    """TimeSeries Analyses section viewlet for Sample view"""

    title = _("Timeseries Results")
    icon_name = "client"
    capture = "timeseries"

    def available(self):
        """Returns true if senaite.timeseries is installed and the sample contains
        at least one sensitivity testing analysis or the microorganism
        identification analysis is present
        """
        if not is_installed():
            return False

        # does this have timeseries analyses?
        timeseries_analyses = get_timeseries_analyses(self.context)
        if timeseries_analyses:
            return True

        return False


class ManageResultsView(AnalysesView):
    """Listing view for Time Series results entry"""

    contents_table_template = ViewPageTemplateFile("templates/timeseries_results.pt")

    def __init__(self, context, request):
        super(ManageResultsView, self).__init__(context, request)

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
        # Remove the columns we are not interested in from review_states
        hide = [
            "Method",
            "Instrument",
            "Analyst",
            "DetectionLimitOperand",
            "Specification",
            "Uncertainty",
            "retested",
            "Attachments",
            "DueDate",
            "Hidden",
            "Unit",
        ]

        all_columns = self.columns.keys()
        all_columns = filter(lambda c: c not in hide, all_columns)
        for review_state in self.review_states:
            review_state.update({"columns": all_columns})

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
            if item.get("result_type").startswith("timeseries"):
                newitems.append(item)
                if item["category"] not in cats:
                    cats.append(item["category"])
        logger.info(
            "AnalysisRequestOverride::folderitems: found {} items with timeseries items and {} categories".format(
                len(newitems), len(cats)
            )
        )
        self.categories = cats
        return newitems


def get_timeseries_analyses(sample, short_title=None, skip_invalid=True):
    """Returns the timeseries analyses assigned to the sample passed in and for the
    microorganism name specified, if any
    """
    analyses = sample.getAnalyses(getPointOfCapture="lab")
    analyses = map(api.get_object, analyses)

    if short_title:
        # Filter by microorganism name (short title)
        analyses = filter(lambda a: a.getShortTitle() == short_title, analyses)

    # Skip invalid analyses
    skip = skip_invalid and ["cancelled", "retracted", "rejected"] or []
    analyses = filter(lambda a: api.get_review_status(a) not in skip, analyses)
    analyses = filter(lambda a: a.getResultType() == "timeseries", analyses)
    return analyses
