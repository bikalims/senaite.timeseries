# -*- coding: utf-8 -*-

import collections

from bika.lims import api
from bika.lims import senaiteMessageFactory as _
from bika.lims.utils import get_link_for
from senaite.core.interfaces import IWorksheetTemplate
from .services_widget import ServicesWidget

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


class WorksheetTemplateServicesWidget(ServicesWidget):
    """Listing widget for Worksheet Template Services
    """

    def update(self):
        super(WorksheetTemplateServicesWidget, self).update()

        method_uid = None
        if IWorksheetTemplate.providedBy(self.context):
            method_uid = self.context.getRawRestrictToMethod()

        if method_uid:
            self.contentFilter.update({
                "method_available_uid": method_uid
            })

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _(
                    u"listing_services_column_title",
                    default=u"Service"
                ),
                "index": "sortable_title",
                "sortable": False
            }),
            ("Keyword", {
                "title": _(
                    u"listing_services_column_keyword",
                    default=u"Keyword"
                ),
                "sortable": False
            }),
            ("Methods", {
                "title": _(
                    u"listing_services_column_methods",
                    default=u"Methods"
                ),
                "sortable": False
            }),
            ("Calculation", {
                "title": _(
                    u"listing_services_column_calculation",
                    default=u"Calculation"
                ),
                "sortable": False
            }),
        ))

        self.review_states[0]["columns"] = self.columns.keys()

    def folderitems(self):
        items = ServicesWidget.folderitems(self)
        new_items = []
        cat_remove = None
        keep = False
        for item in items:
            if item['obj'].getObject().getResultType() == 'timeseries':
                cat_remove = item['obj'].getObject().getCategoryTitle()
                continue
            if item['obj'].getObject().getCategoryTitle() == cat_remove:
                keep = True
            new_items.append(item)
        if cat_remove and keep is False:
            self.categories.pop(self.categories.index(cat_remove))
        return new_items

    def folderitem(self, obj, item, index):
        item = super(WorksheetTemplateServicesWidget, self).folderitem(
            obj, item, index)

        obj = api.get_object(obj)
        cat = obj.getCategoryTitle()
        cat_order = self.an_cats_order.get(cat)

        # NOTE:  get the category
        if self.show_categories_enabled():
            category = obj.getCategoryTitle()
            if (category, cat_order) not in self.categories:
                self.categories.append((category, cat_order))
            item["category"] = category

        calculation = obj.getCalculation()
        if calculation:
            item["Calculation"] = api.get_title(calculation)
            item["replace"]["Calculation"] = get_link_for(calculation)
        else:
            item["Calculation"] = ""

        return item
