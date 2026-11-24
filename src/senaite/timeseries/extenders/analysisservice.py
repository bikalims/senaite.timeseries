from bika.lims import api


def patched_toggle_result_type(self, result_type):
    """Toggle Timeseries fields while preserving the core form behavior."""
    if result_type and api.is_list(result_type):
        result_type = result_type[0]

    is_timeseries = result_type == "timeseries"
    # Timeseries has no result options or manual detection limits.
    self._old_toggle_result_type("text" if is_timeseries else result_type)

    standard_fields = ("DefaultResult", "InterimFields")
    timeseries_fields = (
        "TimeSeriesColumns", "GraphInterpolation", "GraphTitle",
        "GraphXAxisTitle", "GraphYAxisTitle",
    )
    show, hide = standard_fields, timeseries_fields
    if is_timeseries:
        show, hide = hide, show
    for field in show:
        self.add_show_field(field)
    for field in hide:
        self.add_hide_field(field)


def patched_can_change_keyword(self, keyword):
    """Check if the keyword can be changed

    Writable if no active analyses exist with the given keyword
    """
    # patched because it fixes bug in original
    print("patched_can_change_keyword: " + str(keyword))
    query = {
        "portal_type": "Analysis",
        "is_active": True,
        "getKeyword": str(keyword),  # Bugfix
    }
    brains = self.analysis_catalog(query)
    return len(brains) == 0
