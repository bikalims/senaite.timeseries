# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from bika.lims.interfaces import IBikaLIMS


class ISenaiteTimeseriesLayer(IBikaLIMS):
    """Zope 3 browser Layer interface specific for senaite.sampleimporter
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """


class ISenaiteTimeseriesBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
