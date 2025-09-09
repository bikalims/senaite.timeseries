# -*- coding: utf-8 -*-

from bika.lims.browser.worksheet.views.add_analyses import (
    AddAnalysesView as AAV
)


class AddAnalysesView(AAV):
    def folderitems(self):
        items = AAV.folderitems(self)
        new_items = []
        for item in items:
            if item['obj'].getObject().getResultType() == 'timeseries':
                continue
            new_items.append(item)
        return new_items
