## senaite.timeseries

**Time Series Results Add-on for Senaite / Ingwe Bika LIMS**

This add-on extends **Senaite** (the modern core of Bika LIMS) with powerful time-series functionality for laboratory results that evolve over time.

### What is senaite.timeseries?

`senaite.timeseries` allows labs to capture, view, and analyse results that are measured repeatedly on the same sample or object at different time points.

It is particularly useful for:

- Concrete compressive strength testing (7, 28, 56, 90-day breaks)
- Stability studies and shelf-life testing
- Environmental monitoring (e.g. water quality trends)
- Long-term product or material testing
- Trend analysis and graphical reporting

### Key Features

- Capture multiple results for the same analysis at different time intervals
- Beautiful tabular and graphical (chart) presentation of time-series data
- Configurable time points per analysis or sample type
- Trend visualisation directly in the LIMS interface
- Export of time-series data and charts
- Full integration with Senaite workflows, calculations, and reporting
- Audit trail and ISO-compliant data integrity

### Requirements

- **Senaite** (latest recommended) or **Ingwe Bika LIMS 4**
- Python 3 + Plone 6 environment

### Installation

#### For Ingwe Bika LIMS 4 (Docker – Recommended)

Add `senaite.timeseries` to your custom add-ons list in the Ingwe Bika Docker configuration.

##### Classic Buildout

Add the package to your `buildout.cfg`:

cfg
[buildout]
eggs =
    ...
    senaite.timeseries

##### For Docker

### Documentation
Full documentation and configuration guides are available at:
https://www.bikalims.org

### License
This project is licensed under the GNU General Public License v2.0 (GPL-2.0).
See LICENSE.GPL for details.

### Support & Professional Services
Bika Lab Systems provides professional implementation, training, custom development, and ongoing support for senaite.timeseries and the full Ingwe Bika LIMS suite.

Website: https://www.bikalims.org
Based in Cape Town, South Africa


Made with ❤️ in Cape Town, South Africa
