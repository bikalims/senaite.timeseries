# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from senaite.core.catalog import SETUP_CATALOG
from senaite.core.setuphandlers import setup_other_catalogs
from senaite.timeseries.config import PROFILE_ID
from senaite.timeseries.config import logger


# Tuples of (catalog, index_name, index_attribute, index_type)
INDEXES = []

# Tuples of (catalog, column_name)
COLUMNS = [
    (SETUP_CATALOG, "getTimeSeriesColumns"),
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
