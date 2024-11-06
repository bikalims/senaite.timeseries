from bika.lims import api


def patched_toggle_result_type(self, result_type):
    """Hides/Show result options depending on the resulty type"""
    # patched because couldn't get this code to work in a override
    # I think is has something to do with the editing vias
    # the bespoke editform.js and IAjaxEditForm
    if result_type and api.is_list(result_type):
        result_type = str(result_type[0])

    print("patched_toggle_result_type: " + str(result_type))
    if result_type in ["numeric", "string", "text"]:
        self.add_show_field("DefaultResult")
        self.add_show_field("InterimFields")
        self.add_hide_field("ResultOptions")
        self.add_hide_field("ResultOptionsSorting")
        self.add_hide_field("TimeSeriesColumns")
        self.add_hide_field("GraphTitle")
        self.add_hide_field("GraphXAxisTitle")
        self.add_hide_field("GraphYAxisTitle")
    elif result_type == "timeseries":
        self.add_hide_field("DefaultResult")
        self.add_hide_field("InterimFields")
        self.add_hide_field("ResultOptions")
        self.add_hide_field("ResultOptionsSorting")
        self.add_show_field("TimeSeriesColumns")
        self.add_show_field("GraphTitle")
        self.add_show_field("GraphXAxisTitle")
        self.add_show_field("GraphYAxisTitle")
    else:
        self.add_show_field("DefaultResult")
        self.add_show_field("InterimFields")
        self.add_show_field("ResultOptions")
        self.add_show_field("ResultOptionsSorting")
        self.add_hide_field("TimeSeriesColumns")
        self.add_hide_field("GraphTitle")
        self.add_hide_field("GraphXAxisTitle")
        self.add_hide_field("GraphYAxisTitle")


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
