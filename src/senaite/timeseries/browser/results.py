# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.AST.
#
# SENAITE.AST is free software: you can redistribute it and/or modify it under
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
from bika.lims.utils import get_image
from plone.memoize import view
from senaite.timeseries.config import is_installed
from senaite.timeseries.config import _
from senaite.timeseries.browser.overrides.analysisrequest import AnalysesView
from senaite.core.api import dtime
from senaite.core.permissions import ViewResults
# from senaite.ast import utils
# from senaite.ast.config import AST_POINT_OF_CAPTURE
# from senaite.ast.config import IDENTIFICATION_KEY
# from senaite.ast.utils import get_ast_analyses
# from senaite.ast.i18n import translate as t
from senaite.core.browser.viewlets.sampleanalyses import LabAnalysesViewlet


class ASTAnalysesViewlet(LabAnalysesViewlet):
    """AST Analyses section viewlet for Sample view
    """
    title = _("Timeseries Results")
    icon_name = "client"
    capture = "timeseries"

    def available(self):
        """Returns true if senaite.ast is installed and the sample contains
        at least one sensitivity testing analysis or the microorganism
        identification analysis is present
        """
        return True
        if not is_installed():
            return False

        # does this sample has the identification analysis?
        analyses = self.context.getAnalyses(getKeyword=IDENTIFICATION_KEY)
        if analyses:
            return True

        # does this have sensitivity testing analyses?
        ast_analyses = get_ast_analyses(self.context)
        if ast_analyses:
            return True

        return False


class ManageResultsView(AnalysesView):
    """Listing view for AST results entry
    """
    def __init__(self, context, request):
        super(ManageResultsView, self).__init__(context, request)

        self.contentFilter.update({
            "getPointOfCapture": "lab",
            "getAncestorsUIDs": [api.get_uid(context)]
        })

        self.form_id = "%s_lab_analyses" % api.get_id(context)
        self.allow_edit = True
        self.show_workflow_action_buttons = True
        self.show_select_column = True
        self.show_search = False
        self.expand_all_categories = False
        self.reorder_analysis_columns()
        # Remove the columns we are not interested in from review_states
        hide = ["Method", "Instrument", "Analyst", "DetectionLimitOperand",
                "Specification", "Uncertainty", "retested", "Attachments",
                "DueDate", "Hidden", "Unit"]

        all_columns = self.columns.keys()
        all_columns = filter(lambda c: c not in hide, all_columns)
        for review_state in self.review_states:
            review_state.update({"columns": all_columns})
