# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.core.browser.modals.sample import CreateWorksheetModal as CWM


class CreateWorksheetModal(CWM):

    def get_analysis_categories(self):
        """Return analysis categories of the selected samples

        :returns: List available categories for the selected samples
        """
        super(CreateWorksheetModal, self).get_analysis_categories()
        categories = []
        for sample in self.get_selected_samples():
            for analysis in sample.getAnalyses(full_objects=True):
                # timeseries categories are not considered
                result_type = analysis.getResultType()
                if result_type == 'timeseries':
                    continue
                # only consider unassigned analyses
                if api.get_workflow_status_of(analysis) != "unassigned":
                    continue
                # get the category of the analysis
                category = analysis.getCategory()
                if category in categories:
                    continue
                categories.append(category)

        categories = list(map(self.get_category_info,
                          sorted(categories, key=lambda c: c.getSortKey())))
        return categories
