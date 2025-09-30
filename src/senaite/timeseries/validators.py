from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from senaite.core.i18n import translate as _t
from senaite.timeseries.config import _
from zope.interface import implements
import re


def is_valid_color_string(color_string):
    pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(pattern, color_string))


class TimeSeriesValidator:
    """Validate IdentifierTypeAttributes to ensure that attributes are
    not duplicated.
    """

    implements(IValidator)
    name = "timeseriesvalidator"

    def __call__(self, value, *args, **kwargs):
        instance = kwargs["instance"]
        request = instance.REQUEST
        form = request.form
        if form.get("ResultType") != "timeseries":
            return True
        fieldname = kwargs["field"].getName()
        form_values = form.get(fieldname, False)

        # Must have one and only one index column
        index_col_types = [
            col["ColumnType"]
            for col in form_values
            if col["ColumnType"] == "index"
        ]
        if len(index_col_types) == 0 or len(index_col_types) > 1:
            return _t(_("One and only one index column is required"))

        # No more than 1 average column
        ave_col_types = [
            col["ColumnType"]
            for col in form_values
            if col["ColumnType"] == "average"
        ]
        if len(ave_col_types) > 1:
            return _t(_("At most one Average column is allowed"))

        # Text columns must be hidden on plot
        for col in form_values:
            if col["ColumnDataType"] == "text" and not col.get(
                "ColumnHide", False
            ):
                return _t(_("Text columns must be hidden from plot"))

        # Error bar col must have an ave col
        error_col_types = [
            col["ColumnType"]
            for col in form_values
            if col["ColumnType"] == "errorbar"
        ]
        if len(error_col_types) > 1:
            return _t(_("Only one Error Bar column allowed"))

        if len(error_col_types) == 1 and len(ave_col_types) == 0:
            return _t(
                _(
                    "If Error Bar column specified then an Average column in required"
                )
            )

        return True


validation.register(TimeSeriesValidator())


class TimeSeriesTitleValidator:
    """Validate IdentifierTypeAttributes to ensure that attributes are
    not duplicated.
    """

    implements(IValidator)
    name = "timeseriestitlevalidator"

    def __call__(self, value, *args, **kwargs):
        instance = kwargs["instance"]
        request = instance.REQUEST
        form = request.form
        if form.get("ResultType") != "timeseries":
            return True
        fieldname = kwargs["field"].getName()
        form_values = form.get(fieldname, False)

        # Column title must have a value
        empty_titles = False
        for col in form_values:
            title = col.get("ColumnTitle")
            if title is None or len(title) == 0:
                empty_titles = True
        if empty_titles:
            return _t(_("Column Title must have a value"))
        return True


validation.register(TimeSeriesTitleValidator())


class TimeSeriesColorValidator:
    """Ensure column color is valid color."""

    implements(IValidator)
    name = "timeseriescolorvalidator"

    def __call__(self, value, *args, **kwargs):
        instance = kwargs["instance"]
        request = instance.REQUEST
        form = request.form
        if form.get("ResultType") != "timeseries":
            return True
        fieldname = kwargs["field"].getName()
        form_values = form.get(fieldname, False)

        # Column colors must be a valid color string
        for idx, col in enumerate(form_values):
            col_num = idx + 1
            color = col.get("ColumnColor", "")
            if len(color) > 0 and not is_valid_color_string(color):
                return _t(
                    _("Column {} has invalid Color {}".format(col_num, color))
                )
        return True


validation.register(TimeSeriesColorValidator())
