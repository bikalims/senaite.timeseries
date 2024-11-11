# -*- coding: utf-8 -*-

from senaite.core.browser.viewlets.sampleanalyses import LabAnalysesViewlet as LAV
from senaite.timeseries.browser.results import get_timeseries_analyses


class LabAnalysesViewlet(LAV):
    def available(self):
        """Returns a boolean if the len(sample analyses) by point of capture
           is equal to len(timeseries_analyses), meaning there are only
           timeseries analyses.
        """
        analyses = self.sample.getAnalyses(getPointOfCapture=self.capture)
        timeseries_analyses = get_timeseries_analyses(self.sample)
        return len(analyses) != len(timeseries_analyses)
