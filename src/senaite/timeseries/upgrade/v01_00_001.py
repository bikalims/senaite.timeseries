# -*- coding: utf-8 -*-
#
# This file is part of SENAITE
#
# SENAITE.TIMESERIES is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2019-2021 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from senaite.timeseries.config import PRODUCT_NAME
from senaite.timeseries.config import PROFILE_ID
from senaite.timeseries.config import logger
from senaite.timeseries.setuphandlers import setup_catalogs

from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.upgrade import upgradestep

version = "1.0.2"


@upgradestep(PRODUCT_NAME, version)
def upgrade(tool):
    ver_from = "1000"

    portal = api.get_portal()
    setup = portal.portal_setup

    logger.info(
        "Upgrading {0}: {1} -> {2}".format(PRODUCT_NAME, ver_from, version)
    )

    # -------- ADD YOUR STUFF BELOW --------

    setup.runImportStepFromProfile(PROFILE_ID, "typeinfo")

    add_graphinterpolation_to_catalog(tool)

    logger.info("{0} upgraded to version {1}".format(PRODUCT_NAME, version))
    return True


def add_graphinterpolation_to_catalog(tool):
    logger.info("Reindexing timeseries AnalysisService ...")
    setup_catalogs(api.get_portal())
    cat = api.get_tool(SAMPLE_CATALOG)
    for brain in cat(portal_type="AnalysisRequest"):
        sample = brain.getObject()
        analyses = sample.getAnalyses()
        for analysis in analyses:
            obj = analysis.getObject()
            if not hasattr(obj, "GraphInterpolation"):
                obj.GraphInterpolation = "curveLinear"

            if hasattr(obj, "TimeSeriesColumns"):
                for col in obj.TimeSeriesColumns:
                    col["ColumnColor"] = "#000"

            logger.info("Reindex Analysis: %r" % obj)
            obj.reindexObject()
    logger.info("Reindexing timeseries AnalysisService completed")
