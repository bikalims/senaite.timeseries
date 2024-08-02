# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import senaite.timeseries


class SenaiteTimeseriesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=senaite.timeseries)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'senaite.timeseries:default')


SENAITE_TIMESERIES_FIXTURE = SenaiteTimeseriesLayer()


SENAITE_TIMESERIES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SENAITE_TIMESERIES_FIXTURE,),
    name='SenaiteTimeseriesLayer:IntegrationTesting',
)


SENAITE_TIMESERIES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SENAITE_TIMESERIES_FIXTURE,),
    name='SenaiteTimeseriesLayer:FunctionalTesting',
)


SENAITE_TIMESERIES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SENAITE_TIMESERIES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='SenaiteTimeseriesLayer:AcceptanceTesting',
)
