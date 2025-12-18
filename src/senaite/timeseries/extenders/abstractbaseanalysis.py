# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Widget import SelectionWidget
from Products.Archetypes.utils import DisplayList
from Products.CMFCore import permissions
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.component import adapts
from zope.interface import implementer
from zope.interface import implements

from .fields import ExtStringField, ExtRecordsField
from bika.lims.browser.widgets.recordswidget import RecordsWidget
from bika.lims.interfaces import IBaseAnalysis
from senaite.timeseries.config import _
from senaite.timeseries.config import is_installed
from senaite.timeseries.vocabularies import INTERPOLCATIONS
from senaite.timeseries.vocabularies import RESULT_TYPES
from senaite.timeseries.interfaces import ISenaiteTimeseriesLayer


# Type of control to be rendered on results entry
graph_interpolation = ExtStringField(
    "GraphInterpolation",
    schemata="Result Options",
    default="curveBasis",
    vocabulary=DisplayList(INTERPOLCATIONS),
    accessor="getGraphInterpolation",
    widget=SelectionWidget(
        label=_("Interpolation"),
        format="select",
    ),
)


graph_title_field = ExtStringField(
    "GraphTitle",
    schemata="Result Options",
    widget=StringWidget(
        label=_("Graph Title"),
        description=_("Title that appears above the time series graph"),
    ),
)
graph_x_axis_title_field = ExtStringField(
    "GraphXAxisTitle",
    schemata="Result Options",
    widget=StringWidget(
        label=_("Graph X-Axis Title"),
        description=_(
            "Title that appears on the X-Axis of the time series graph"
        ),
    ),
)
graph_y_axis_title_field = ExtStringField(
    "GraphYAxisTitle",
    schemata="Result Options",
    widget=StringWidget(
        label=_("Graph Y-Axis Title"),
        description=_(
            "Title that appears on the Y-Axis of the time series graph"
        ),
    ),
)
time_series_columns_field = ExtRecordsField(
    "TimeSeriesColumns",
    schemata="Result Options",
    validators=(
        "timeseriesvalidator",
        "timeseriestitlevalidator",
        "timeseriescolorvalidator",
        "timeserieshidevalidator",
    ),
    subfields=(
        "ColumnType",
        "ColumnTitle",
        "ColumnDataType",
        "ColumnColor",
        "ColumnHide",
    ),
    subfield_labels={
        "ColumnType": _("Column Type"),
        "ColumnTitle": _("Column Title"),
        "ColumnDataType": _("Column Data Type"),
        "ColumnColor": _("Column Color"),
        "ColumnHide": _("Hide on plot"),
    },
    subfield_validators={
        "ColumnType": "timeseriesvalidator",
        "ColumnTitle": "timeseriestitlevalidator",
        "ColumnColor": "timeseriescolorvalidator",
        "ColumnHide": "timeserieshidevalidator",
    },
    subfield_types={
        "ColumnType": "string",
        "ColumnTitle": "string",
        "ColumnDataType": "string",
        "ColumnColor": "string",
        "ColumnHide": "boolean",
    },
    subfield_sizes={
        "ColumnType": 1,
        # 'ColumnTitle': 25,
        "ColumnDataType": 1,
        # "ColumnColor": 8,
    },
    subfield_maxlength={
        "ColumnType": 1,
        "ColumnTitle": 25,
        "ColumnDataType": 1,
        "ColumnColor": 8,
        "ColumnHide": 4,
    },
    subfield_vocabularies={
        "ColumnType": DisplayList(
            (
                ("", ""),
                ("index", _("Index")),
                ("data", _("Data")),
                ("errorbar", _("Error Bar")),
                ("average", _("Average")),
            )
        ),
        "ColumnDataType": DisplayList(
            (
                ("", ""),
                ("float", _("Float")),
                ("number", _("Number")),
                ("text", _("Text")),
                # ("date", _("Date")),
            )
        ),
    },
    widget=RecordsWidget(
        label=_("Time Series Columns"),
        description=_(
            "List of possible final results. When set, no custom result is "
            "allowed on results entry and user has to choose from these values"
        ),
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BaseAnalysisSchemaExtender(object):
    adapts(IBaseAnalysis)
    layer = ISenaiteTimeseriesLayer

    security = ClassSecurityInfo()

    fields = [
        graph_interpolation,
        graph_title_field,
        graph_x_axis_title_field,
        graph_y_axis_title_field,
        time_series_columns_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

    @security.protected(permissions.View)
    def getGraphInterpolation(self):
        accessor = self.accessor("GraphInterpolation")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setGraphInterpolation(self, value):
        mutator = self.mutator("GraphInterpolation")
        mutator(self, value)

    @security.protected(permissions.View)
    def getGraphTitle(self):
        accessor = self.accessor("GraphTitle")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setGraphTitle(self, value):
        mutator = self.mutator("GraphTitle")
        mutator(self, value)


class BaseAnalysisSchemaModifier(object):
    adapts(IBaseAnalysis)
    implements(ISchemaModifier)
    layer = ISenaiteTimeseriesLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """ """
        if is_installed():
            schema["ResultType"].vocabulary = DisplayList(RESULT_TYPES)

        return schema
