# -*- coding: utf-8 -*-

from bika.lims.api import get_request
import logging
from senaite.timeseries.interfaces import ISenaiteTimeseriesLayer
from zope.i18nmessageid import MessageFactory

PRODUCT_NAME = "senaite.timeseries"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)
logger = logging.getLogger(PRODUCT_NAME)
_ = MessageFactory(PRODUCT_NAME)


def is_installed():
    """Returns whether the product is installed or not"""
    request = get_request()
    return ISenaiteTimeseriesLayer.providedBy(request)
