# -*- coding: utf-8 -*-

from senaite.timeseries.config import _

RESULT_TYPES = (
    ("numeric", _("Numeric")),
    ("string", _("String")),
    ("text", _("Text")),
    ("select", _("Selection list")),
    ("multiselect", _("Multiple selection")),
    ("multiselect_duplicates", _("Multiple selection (with duplicates)")),
    ("multichoice", _("Multiple choices")),
    ("multivalue", _("Multiple values")),
    ("timeseries", _("Time series")),
)

INTERPOLCATIONS = (
    ("curveBasis", _("Basis")),
    ("curveCardinal", _("Cardinal")),
    ("curveLinear", _("Linear")),
)
