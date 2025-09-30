# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.setuphandlers import setup_other_catalogs
from senaite.timeseries.config import PROFILE_ID
from senaite.timeseries.config import logger


# Tuples of (catalog, index_name, index_attribute, index_type)
INDEXES = []

# Tuples of (catalog, column_name)
COLUMNS = [
    (SETUP_CATALOG, "getTimeSeriesColumns"),
    (SETUP_CATALOG, "getGraphInterpolation"),
    (SETUP_CATALOG, "getGraphTitle"),
    (SETUP_CATALOG, "getGraphXAxisTitle"),
    (SETUP_CATALOG, "getGraphYAxisTitle"),
]


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "senaite.timeseries:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    logger.info("SENAITE.TIMESERIES post install handler [BEGIN]")
    context = context._getImportContext(PROFILE_ID)
    portal = context.getSite()
    setup_catalogs(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setup_catalogs(portal):
    """Setup patient catalogs"""
    setup_other_catalogs(portal, indexes=INDEXES, columns=COLUMNS)


def add_attachment_to_sample(portal):
    pt = api.get_tool("portal_types", context=portal)
    fti = pt.get("AnalysisRequest")

    # add to allowed types
    allowed_types = fti.allowed_content_types
    if isinstance(allowed_types, tuple) or isinstance(allowed_types, list):
        allowed_types = list(allowed_types)
        if "Attachment" not in allowed_types:
            allowed_types.append("Attachment")
            fti.allowed_content_types = tuple(allowed_types)
            logger.info("Add Attachment on AnalysisRequest allowed types")
